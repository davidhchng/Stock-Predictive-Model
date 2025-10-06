/**
 * Interactive price chart component using Plotly
 */

import React, { useState, useEffect, useCallback } from 'react';
import Plot from 'react-plotly.js';
import {
  Box,
  Paper,
  Typography,
  ToggleButtonGroup,
  ToggleButton,
  CircularProgress,
  Alert,
  Chip,
  Grid,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  ShowChart,
  Candlestick,
  BarChart,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const PriceChart = ({ ticker, onDataLoaded }) => {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chartType, setChartType] = useState('candlestick');
  const [showIndicators, setShowIndicators] = useState(true);
  const [currentPrice, setCurrentPrice] = useState(null);
  const [priceChange, setPriceChange] = useState(null);

  // Load chart data when ticker changes
  useEffect(() => {
    if (ticker) {
      loadChartData();
    }
  }, [ticker]);

  const loadChartData = async () => {
    if (!ticker) return;

    setLoading(true);
    setError(null);

    try {
      // Get historical data for the last 6 months
      const endDate = new Date();
      const startDate = new Date();
      startDate.setMonth(startDate.getMonth() - 6);

      const stockData = await apiService.getStockData(
        ticker,
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0]
      );

      if (stockData && stockData.length > 0) {
        processChartData(stockData);
        
        // Set current price info
        const latest = stockData[stockData.length - 1];
        setCurrentPrice(latest.close);
        
        // Calculate price change from first to last
        const first = stockData[0];
        const change = ((latest.close - first.close) / first.close) * 100;
        setPriceChange(change);

        // Notify parent component
        if (onDataLoaded) {
          onDataLoaded(stockData);
        }
      } else {
        setError('No data available for the selected stock');
      }
    } catch (err) {
      setError(`Failed to load chart data: ${err.message}`);
      console.error('Error loading chart data:', err);
    } finally {
      setLoading(false);
    }
  };

  const processChartData = (data) => {
    const dates = data.map(d => d.date);
    const opens = data.map(d => d.open);
    const highs = data.map(d => d.high);
    const lows = data.map(d => d.low);
    const closes = data.map(d => d.close);
    const volumes = data.map(d => d.volume);

    let traces = [];

    if (chartType === 'candlestick') {
      traces.push({
        x: dates,
        open: opens,
        high: highs,
        low: lows,
        close: closes,
        type: 'candlestick',
        name: 'Price',
        increasing: { line: { color: '#26a69a' } },
        decreasing: { line: { color: '#ef5350' } },
      });
    } else if (chartType === 'line') {
      traces.push({
        x: dates,
        y: closes,
        type: 'scatter',
        mode: 'lines',
        name: 'Close Price',
        line: { color: '#1976d2', width: 2 },
      });
    }

    // Add volume bars
    traces.push({
      x: dates,
      y: volumes,
      type: 'bar',
      name: 'Volume',
      yaxis: 'y2',
      marker: { color: 'rgba(158,158,158,0.3)' },
      showlegend: false,
    });

    // Add moving averages if enabled
    if (showIndicators) {
      const ma20 = calculateMovingAverage(closes, 20);
      const ma50 = calculateMovingAverage(closes, 50);

      traces.push({
        x: dates,
        y: ma20,
        type: 'scatter',
        mode: 'lines',
        name: 'MA 20',
        line: { color: '#ff9800', width: 1, dash: 'dash' },
      });

      traces.push({
        x: dates,
        y: ma50,
        type: 'scatter',
        mode: 'lines',
        name: 'MA 50',
        line: { color: '#9c27b0', width: 1, dash: 'dot' },
      });
    }

    setChartData(traces);
  };

  const calculateMovingAverage = (data, period) => {
    const result = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        result.push(null);
      } else {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        result.push(sum / period);
      }
    }
    return result;
  };

  const handleChartTypeChange = (event, newType) => {
    if (newType !== null) {
      setChartType(newType);
    }
  };

  const handleIndicatorsChange = (event, newIndicators) => {
    setShowIndicators(newIndicators);
  };

  const layout = {
    title: {
      text: `${ticker} - Price Chart`,
      font: { size: 18 },
    },
    xaxis: {
      title: 'Date',
      type: 'date',
      rangeslider: { visible: false },
    },
    yaxis: {
      title: 'Price ($)',
      side: 'left',
    },
    yaxis2: {
      title: 'Volume',
      side: 'right',
      overlaying: 'y',
      showticklabels: false,
    },
    legend: {
      orientation: 'h',
      x: 0,
      y: 1.02,
      xanchor: 'left',
      yanchor: 'bottom',
    },
    margin: { l: 50, r: 50, t: 80, b: 50 },
    hovermode: 'x unified',
    responsive: true,
    showlegend: true,
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    displaylogo: false,
  };

  if (loading) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body2" sx={{ mt: 2 }}>
          Loading chart data...
        </Typography>
      </Paper>
    );
  }

  if (error) {
    return (
      <Paper sx={{ p: 3 }}>
        <Alert severity="error">{error}</Alert>
      </Paper>
    );
  }

  if (!chartData) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body1" color="text.secondary">
          Select a stock to view the price chart
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 2 }}>
      {/* Chart Controls */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="h6" component="div">
            Price Chart
          </Typography>
          {currentPrice && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="h6" fontWeight="bold">
                ${currentPrice.toFixed(2)}
              </Typography>
              {priceChange !== null && (
                <Chip
                  icon={priceChange >= 0 ? <TrendingUp /> : <TrendingDown />}
                  label={`${priceChange >= 0 ? '+' : ''}${priceChange.toFixed(2)}%`}
                  color={priceChange >= 0 ? 'success' : 'error'}
                  size="small"
                />
              )}
            </Box>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <ToggleButtonGroup
            value={chartType}
            exclusive
            onChange={handleChartTypeChange}
            size="small"
          >
            <ToggleButton value="candlestick" aria-label="candlestick">
              <Candlestick fontSize="small" />
            </ToggleButton>
            <ToggleButton value="line" aria-label="line">
              <ShowChart fontSize="small" />
            </ToggleButton>
          </ToggleButtonGroup>

          <ToggleButtonGroup
            value={showIndicators}
            exclusive
            onChange={handleIndicatorsChange}
            size="small"
          >
            <ToggleButton value={true} aria-label="show indicators">
              <BarChart fontSize="small" />
            </ToggleButton>
          </ToggleButtonGroup>
        </Box>
      </Box>

      {/* Chart */}
      <Box sx={{ height: 500 }}>
        <Plot
          data={chartData}
          layout={layout}
          config={config}
          style={{ width: '100%', height: '100%' }}
          onUpdate={(figure) => setChartData(figure.data)}
        />
      </Box>
    </Paper>
  );
};

export default PriceChart;

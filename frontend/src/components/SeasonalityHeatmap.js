/**
 * Seasonality heatmap component showing monthly/quarterly patterns
 */

import React, { useState, useEffect } from 'react';
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
  Card,
  CardContent,
} from '@mui/material';
import {
  CalendarMonth,
  TrendingUp,
  TrendingDown,
  Assessment,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const SeasonalityHeatmap = ({ ticker }) => {
  const [heatmapData, setHeatmapData] = useState(null);
  const [seasonalityData, setSeasonalityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [periodType, setPeriodType] = useState('monthly');

  // Load seasonality data when ticker changes
  useEffect(() => {
    if (ticker) {
      loadSeasonalityData();
    }
  }, [ticker, periodType]);

  const loadSeasonalityData = async () => {
    if (!ticker) return;

    setLoading(true);
    setError(null);

    try {
      // Load both heatmap and detailed seasonality data
      const [heatmapResponse, seasonalityResponse] = await Promise.all([
        apiService.getSeasonalityHeatmap(ticker, periodType),
        apiService.getSeasonalityAnalysis(ticker)
      ]);

      setHeatmapData(heatmapResponse);
      setSeasonalityData(seasonalityResponse);
    } catch (err) {
      setError(`Failed to load seasonality data: ${err.message}`);
      console.error('Error loading seasonality data:', err);
    } finally {
      setLoading(false);
    }
  };

  const processHeatmapData = (data) => {
    if (!data || typeof data !== 'object') return null;

    // Convert data to format suitable for Plotly heatmap
    const years = Object.keys(data).sort();
    const periods = periodType === 'monthly' 
      ? ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      : ['Q1', 'Q2', 'Q3', 'Q4'];

    const z = [];
    const y = years;
    const x = periods;

    // Fill the z matrix
    for (let i = 0; i < periods.length; i++) {
      const row = [];
      for (let j = 0; j < years.length; j++) {
        const year = years[j];
        const periodKey = periodType === 'monthly' ? i + 1 : i + 1;
        const value = data[year] && data[year][periodKey] !== undefined 
          ? data[year][periodKey] 
          : null;
        row.push(value);
      }
      z.push(row);
    }

    return { x, y, z };
  };

  const handlePeriodTypeChange = (event, newType) => {
    if (newType !== null) {
      setPeriodType(newType);
    }
  };

  const getSeasonalityInsights = () => {
    if (!seasonalityData || !seasonalityData.summary) return null;

    const summary = seasonalityData.summary;
    const insights = [];

    if (summary.best_month) {
      insights.push({
        type: 'best',
        period: summary.best_month.month_name,
        return: summary.best_month.avg_return,
        icon: <TrendingUp />,
        color: 'success'
      });
    }

    if (summary.worst_month) {
      insights.push({
        type: 'worst',
        period: summary.worst_month.month_name,
        return: summary.worst_month.avg_return,
        icon: <TrendingDown />,
        color: 'error'
      });
    }

    return insights;
  };

  const createHeatmapTrace = () => {
    const processedData = processHeatmapData(heatmapData);
    
    if (!processedData) return null;

    return {
      x: processedData.x,
      y: processedData.y,
      z: processedData.z,
      type: 'heatmap',
      colorscale: [
        [0, '#ef5350'],  // Red for negative returns
        [0.5, '#ffffff'], // White for neutral
        [1, '#26a69a']   // Green for positive returns
      ],
      zmid: 0,
      hovertemplate: '<b>%{y}</b><br>%{x}<br>Return: %{z:.3f}<extra></extra>',
      showscale: true,
      colorbar: {
        title: 'Average Return',
        titleside: 'right',
        tickformat: '.1%'
      }
    };
  };

  const heatmapLayout = {
    title: {
      text: `${ticker} - ${periodType === 'monthly' ? 'Monthly' : 'Quarterly'} Seasonality`,
      font: { size: 16 }
    },
    xaxis: {
      title: periodType === 'monthly' ? 'Month' : 'Quarter',
      side: 'bottom'
    },
    yaxis: {
      title: 'Year',
      autorange: 'reversed'
    },
    margin: { l: 60, r: 60, t: 60, b: 60 },
    height: 400,
  };

  const insights = getSeasonalityInsights();

  if (loading) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body2" sx={{ mt: 2 }}>
          Loading seasonality data...
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

  if (!heatmapData) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body1" color="text.secondary">
          Select a stock to view seasonality patterns
        </Typography>
      </Paper>
    );
  }

  const heatmapTrace = createHeatmapTrace();

  return (
    <Paper sx={{ p: 2 }}>
      {/* Header */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6" component="div">
          Seasonality Analysis
        </Typography>
        
        <ToggleButtonGroup
          value={periodType}
          exclusive
          onChange={handlePeriodTypeChange}
          size="small"
        >
          <ToggleButton value="monthly" aria-label="monthly">
            <CalendarMonth fontSize="small" />
            Monthly
          </ToggleButton>
          <ToggleButton value="quarterly" aria-label="quarterly">
            <Assessment fontSize="small" />
            Quarterly
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Insights Cards */}
      {insights && insights.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Grid container spacing={2}>
            {insights.map((insight, index) => (
              <Grid item xs={6} key={index}>
                <Card variant="outlined">
                  <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {insight.icon}
                      <Typography variant="body2" fontWeight="bold">
                        {insight.type === 'best' ? 'Best' : 'Worst'} Period:
                      </Typography>
                    </Box>
                    <Typography variant="body1" fontWeight="bold">
                      {insight.period}
                    </Typography>
                    <Chip
                      label={`${(insight.return * 100).toFixed(2)}%`}
                      color={insight.color}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Heatmap */}
      <Box sx={{ height: 450 }}>
        {heatmapTrace && (
          <Plot
            data={[heatmapTrace]}
            layout={heatmapLayout}
            config={{
              responsive: true,
              displayModeBar: false,
            }}
            style={{ width: '100%', height: '100%' }}
          />
        )}
      </Box>

      {/* Legend */}
      <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="caption" color="text.secondary">
          <strong>Heatmap Legend:</strong> Red indicates negative average returns, 
          green indicates positive average returns. The intensity of the color 
          represents the magnitude of the return.
        </Typography>
      </Box>
    </Paper>
  );
};

export default SeasonalityHeatmap;

/**
 * Main App component for S&P 500 Stock Analysis Tool
 */

import React, { useState } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Box,
  Grid,
  Paper,
  Typography,
  Alert,
  Snackbar,
} from '@mui/material';
import Header from './components/Header';
import StockSelector from './components/StockSelector';
import PriceChart from './components/PriceChart';
import SeasonalityHeatmap from './components/SeasonalityHeatmap';
import PredictionPanel from './components/PredictionPanel';
import AboutDialog from './components/AboutDialog';

// Create Material-UI theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [chartData, setChartData] = useState(null);

  const handleTickerChange = (ticker) => {
    setSelectedTicker(ticker);
    if (ticker) {
      setSnackbarMessage(`Now analyzing ${ticker}`);
      setSnackbarOpen(true);
    }
  };

  const handleChartDataLoaded = (data) => {
    setChartData(data);
  };

  const handleInfoClick = () => {
    setAboutOpen(true);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
        <Header 
          selectedTicker={selectedTicker}
          onInfoClick={handleInfoClick}
        />

        <Container maxWidth="xl" sx={{ py: 4 }}>
          {/* Stock Selector */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
              Select Stock to Analyze
            </Typography>
            <StockSelector
              selectedTicker={selectedTicker}
              onTickerChange={handleTickerChange}
            />
          </Paper>

          {selectedTicker ? (
            <Grid container spacing={3}>
              {/* Price Chart - Full Width */}
              <Grid item xs={12}>
                <PriceChart
                  ticker={selectedTicker}
                  onDataLoaded={handleChartDataLoaded}
                />
              </Grid>

              {/* Seasonality Heatmap */}
              <Grid item xs={12} md={8}>
                <SeasonalityHeatmap ticker={selectedTicker} />
              </Grid>

              {/* Prediction Panel */}
              <Grid item xs={12} md={4}>
                <PredictionPanel ticker={selectedTicker} />
              </Grid>
            </Grid>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
                Welcome to S&P 500 Stock Analysis
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Select a stock from the dropdown above to begin your analysis.
                <br />
                Explore trends, seasonality patterns, and AI-powered predictions.
              </Typography>
            </Paper>
          )}
        </Container>

        {/* About Dialog */}
        <AboutDialog
          open={aboutOpen}
          onClose={() => setAboutOpen(false)}
        />

        {/* Snackbar for notifications */}
        <Snackbar
          open={snackbarOpen}
          autoHideDuration={3000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={handleCloseSnackbar} severity="success">
            {snackbarMessage}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}

export default App;

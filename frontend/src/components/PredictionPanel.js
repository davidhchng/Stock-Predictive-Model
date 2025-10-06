/**
 * Prediction panel component showing next day prediction and analysis
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Alert,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Psychology,
  Assessment,
  Info,
  CheckCircle,
  Cancel,
  Warning,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const PredictionPanel = ({ ticker }) => {
  const [predictionData, setPredictionData] = useState(null);
  const [analysisSummary, setAnalysisSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load prediction data when ticker changes
  useEffect(() => {
    if (ticker) {
      loadPredictionData();
    }
  }, [ticker]);

  const loadPredictionData = async () => {
    if (!ticker) return;

    setLoading(true);
    setError(null);

    try {
      // Load both prediction and analysis summary
      const [predictionResponse, summaryResponse] = await Promise.all([
        apiService.getPrediction(ticker),
        apiService.getAnalysisSummary(ticker)
      ]);

      setPredictionData(predictionResponse);
      setAnalysisSummary(summaryResponse);
    } catch (err) {
      setError(`Failed to load prediction data: ${err.message}`);
      console.error('Error loading prediction data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPredictionIcon = (prediction) => {
    switch (prediction) {
      case 'bullish':
        return <TrendingUp />;
      case 'bearish':
        return <TrendingDown />;
      default:
        return <TrendingFlat />;
    }
  };

  const getPredictionColor = (prediction) => {
    switch (prediction) {
      case 'bullish':
        return 'success';
      case 'bearish':
        return 'error';
      default:
        return 'default';
    }
  };

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'high':
        return 'success';
      case 'medium':
        return 'warning';
      case 'low':
        return 'error';
      default:
        return 'default';
    }
  };

  const getConfidenceIcon = (confidence) => {
    switch (confidence) {
      case 'high':
        return <CheckCircle />;
      case 'medium':
        return <Warning />;
      case 'low':
        return <Cancel />;
      default:
        return <Info />;
    }
  };

  const formatProbability = (probability) => {
    return (probability * 100).toFixed(1);
  };

  const getRecommendationIcon = (recommendation) => {
    if (recommendation.toLowerCase().includes('buy')) {
      return <TrendingUp color="success" />;
    } else if (recommendation.toLowerCase().includes('sell')) {
      return <TrendingDown color="error" />;
    } else {
      return <TrendingFlat color="default" />;
    }
  };

  if (loading) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body2" sx={{ mt: 2 }}>
          Loading prediction data...
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

  if (!predictionData || !analysisSummary) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="body1" color="text.secondary">
          Select a stock to view predictions
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Psychology />
        AI Prediction Analysis
      </Typography>

      <Grid container spacing={2}>
        {/* Main Prediction Card */}
        <Grid item xs={12} md={6}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>
                Next Day Prediction
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Chip
                  icon={getPredictionIcon(predictionData.prediction)}
                  label={predictionData.prediction.toUpperCase()}
                  color={getPredictionColor(predictionData.prediction)}
                  size="large"
                />
                
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Probability
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={predictionData.probability * 100}
                    color={getPredictionColor(predictionData.prediction)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                  <Typography variant="h6" fontWeight="bold">
                    {formatProbability(predictionData.probability)}%
                  </Typography>
                </Box>
              </Box>

              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Chip
                  icon={getConfidenceIcon(predictionData.confidence)}
                  label={`${predictionData.confidence.toUpperCase()} CONFIDENCE`}
                  color={getConfidenceColor(predictionData.confidence)}
                  size="small"
                />
              </Box>

              {predictionData.model_used && (
                <Typography variant="caption" color="text.secondary">
                  Model: {predictionData.model_used} | Features: {predictionData.features_analyzed}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Analysis Summary */}
        <Grid item xs={12} md={6}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>
                Overall Analysis
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Sentiment
                </Typography>
                <Chip
                  icon={getPredictionIcon(analysisSummary.overall_sentiment)}
                  label={analysisSummary.overall_sentiment.toUpperCase()}
                  color={getPredictionColor(analysisSummary.overall_sentiment)}
                  size="small"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Confidence Level
                </Typography>
                <Chip
                  icon={getConfidenceIcon(analysisSummary.confidence_level)}
                  label={analysisSummary.confidence_level.toUpperCase()}
                  color={getConfidenceColor(analysisSummary.confidence_level)}
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Key Insights */}
        <Grid item xs={12}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Assessment />
                Key Insights
              </Typography>
              
              {analysisSummary.key_insights && analysisSummary.key_insights.length > 0 ? (
                <List dense>
                  {analysisSummary.key_insights.map((insight, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        <Info color="primary" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={insight}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No specific insights available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 2 }}>
                Recommendations
              </Typography>
              
              {analysisSummary.recommendations && analysisSummary.recommendations.length > 0 ? (
                <List dense>
                  {analysisSummary.recommendations.map((recommendation, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemIcon sx={{ minWidth: 32 }}>
                        {getRecommendationIcon(recommendation)}
                      </ListItemIcon>
                      <ListItemText 
                        primary={recommendation}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No specific recommendations available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {/* Disclaimer */}
      <Alert severity="info" sx={{ mt: 2 }}>
        <Typography variant="caption">
          <strong>Educational Purpose Only:</strong> This prediction is generated by machine learning 
          models based on historical data and technical indicators. It should not be considered as 
          financial advice. Always conduct your own research and consult with financial professionals 
          before making investment decisions. Past performance does not guarantee future results.
        </Typography>
      </Alert>
    </Paper>
  );
};

export default PredictionPanel;

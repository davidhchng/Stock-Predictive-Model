/**
 * About dialog component with information about the tool
 */

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Button,
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Assessment,
  Schedule,
  Security,
  Code,
  DataUsage,
} from '@mui/icons-material';

const AboutDialog = ({ open, onClose }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <TrendingUp color="primary" fontSize="large" />
          <Typography variant="h5" component="div">
            S&P 500 Stock Analysis Tool
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent>
        <Typography variant="body1" paragraph>
          A comprehensive stock analysis platform that combines historical data analysis, 
          seasonal pattern recognition, and AI-powered predictions for S&P 500 companies.
        </Typography>

        <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
          Key Features
        </Typography>

        <List>
          <ListItem>
            <ListItemIcon>
              <Assessment color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Technical Analysis"
              secondary="Moving averages, RSI, MACD, Bollinger Bands, and more"
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <Schedule color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Seasonality Analysis"
              secondary="Monthly and quarterly pattern analysis with interactive heatmaps"
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <Psychology color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="AI Predictions"
              secondary="Machine learning models for next-day price direction prediction"
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <DataUsage color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Real-time Data"
              secondary="Automated daily updates from Yahoo Finance and Wikipedia"
            />
          </ListItem>
        </List>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" sx={{ mb: 2 }}>
          Technology Stack
        </Typography>

        <List>
          <ListItem>
            <ListItemIcon>
              <Code color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Backend"
              secondary="Python, FastAPI, SQLite, scikit-learn, yfinance"
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <Code color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Frontend"
              secondary="React, Material-UI, Plotly.js, Axios"
            />
          </ListItem>

          <ListItem>
            <ListItemIcon>
              <DataUsage color="primary" />
            </ListItemIcon>
            <ListItemText
              primary="Data Sources"
              secondary="Yahoo Finance, Wikipedia S&P 500 list"
            />
          </ListItem>
        </List>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" sx={{ mb: 2 }}>
          Data & Updates
        </Typography>

        <Typography variant="body2" paragraph>
          • Historical data from 2018 to present
          • Automated daily updates via cron jobs
          • Covers all current S&P 500 companies
          • Real-time technical indicators
        </Typography>

        <Alert severity="warning" sx={{ mt: 2 }}>
          <Typography variant="body2">
            <strong>Disclaimer:</strong> This tool is for educational and research purposes only. 
            The predictions and analysis should not be considered as financial advice. 
            Always consult with qualified financial professionals before making investment decisions. 
            Past performance does not guarantee future results.
          </Typography>
        </Alert>

        <Divider sx={{ my: 2 }} />

        <Typography variant="h6" sx={{ mb: 2 }}>
          How to Use
        </Typography>

        <Typography variant="body2" paragraph>
          1. <strong>Select a Stock:</strong> Use the search bar to find any S&P 500 company
        </Typography>

        <Typography variant="body2" paragraph>
          2. <strong>View Price Chart:</strong> Interactive candlestick chart with technical indicators
        </Typography>

        <Typography variant="body2" paragraph>
          3. <strong>Analyze Seasonality:</strong> Explore monthly/quarterly patterns in the heatmap
        </Typography>

        <Typography variant="body2" paragraph>
          4. <strong>Check Predictions:</strong> Review AI-powered next-day predictions and recommendations
        </Typography>

        <Typography variant="body2">
          5. <strong>Make Informed Decisions:</strong> Combine all insights for comprehensive analysis
        </Typography>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} variant="contained">
          Got it!
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AboutDialog;

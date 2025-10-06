/**
 * Header component with title and navigation
 */

import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Assessment,
  Info,
} from '@mui/icons-material';

const Header = ({ selectedTicker, onInfoClick }) => {
  return (
    <AppBar position="static" elevation={1}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexGrow: 1 }}>
          <TrendingUp fontSize="large" />
          <Box>
            <Typography variant="h6" component="div" fontWeight="bold">
              S&P 500 Stock Analysis
            </Typography>
            <Typography variant="caption" component="div" sx={{ opacity: 0.8 }}>
              Trend, Seasonality & AI Prediction Tool
            </Typography>
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {selectedTicker && (
            <Chip
              icon={<Assessment />}
              label={`Analyzing: ${selectedTicker}`}
              color="secondary"
              variant="outlined"
            />
          )}
          
          <Tooltip title="About this tool">
            <IconButton
              color="inherit"
              onClick={onInfoClick}
              size="small"
            >
              <Info />
            </IconButton>
          </Tooltip>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;

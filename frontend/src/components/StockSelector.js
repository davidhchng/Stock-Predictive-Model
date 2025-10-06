/**
 * Stock selector component with search and autocomplete
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Autocomplete,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { apiService } from '../services/api';

const StockSelector = ({ selectedTicker, onTickerChange, disabled = false }) => {
  const [tickers, setTickers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load tickers on component mount
  useEffect(() => {
    loadTickers();
  }, []);

  const loadTickers = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const tickerData = await apiService.getTickers();
      setTickers(tickerData);
    } catch (err) {
      setError('Failed to load stock tickers. Please try again.');
      console.error('Error loading tickers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTickerChange = (event, newValue) => {
    if (newValue && newValue.ticker) {
      onTickerChange(newValue.ticker);
    } else {
      onTickerChange(null);
    }
  };

  const getOptionLabel = (option) => {
    if (typeof option === 'string') {
      return option;
    }
    return `${option.ticker} - ${option.name}`;
  };

  const isOptionEqualToValue = (option, value) => {
    if (option && value) {
      return option.ticker === value.ticker;
    }
    return option === value;
  };

  const filterOptions = (options, { inputValue }) => {
    if (!inputValue) return options.slice(0, 50); // Show first 50 by default
    
    const filtered = options.filter(option =>
      option.ticker.toLowerCase().includes(inputValue.toLowerCase()) ||
      option.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    
    return filtered.slice(0, 50); // Limit to 50 results
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 400 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      <Autocomplete
        value={selectedTicker ? tickers.find(t => t.ticker === selectedTicker) : null}
        onChange={handleTickerChange}
        options={tickers}
        getOptionLabel={getOptionLabel}
        isOptionEqualToValue={isOptionEqualToValue}
        filterOptions={filterOptions}
        loading={loading}
        disabled={disabled}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Select S&P 500 Stock"
            placeholder="Search by ticker or company name..."
            InputProps={{
              ...params.InputProps,
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              endAdornment: (
                <>
                  {loading ? <CircularProgress color="inherit" size={20} /> : null}
                  {params.InputProps.endAdornment}
                </>
              ),
            }}
          />
        )}
        renderOption={(props, option) => (
          <Box component="li" {...props}>
            <Box>
              <Typography variant="body1" fontWeight="bold">
                {option.ticker}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {option.name}
              </Typography>
            </Box>
          </Box>
        )}
        noOptionsText="No stocks found"
        loadingText="Loading stocks..."
        sx={{
          '& .MuiAutocomplete-inputRoot': {
            backgroundColor: 'background.paper',
          },
        }}
      />
    </Box>
  );
};

export default StockSelector;

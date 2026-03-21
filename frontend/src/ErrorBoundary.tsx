import { Component, ReactNode } from 'react';
import { Box, Typography, Button } from '@mui/material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ py: 8, textAlign: 'center' }}>
          <Typography variant="h5" fontWeight={700} gutterBottom>Something went wrong</Typography>
          <Typography color="text.secondary" sx={{ mb: 3 }}>
            An unexpected error occurred. Try refreshing the page.
          </Typography>
          <Button variant="outlined" color="secondary" onClick={() => window.location.reload()}>
            Reload
          </Button>
        </Box>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;

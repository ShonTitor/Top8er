import { useEffect } from 'react';
import { Box, Typography, Paper, Divider, Link } from '@mui/material';
import EmailIcon from '@mui/icons-material/Email';

function ContactPage() {
  useEffect(() => { document.title = 'Top8er | Contact'; }, []);
  return (
    <Box sx={{ py: 4, maxWidth: 600, mx: 'auto' }}>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>Contact</Typography>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          Get in touch
        </Typography>
        <Typography color="text.secondary">
          Have a question, suggestion, or found a bug? Feel free to reach out.
        </Typography>
      </Box>

      <Divider sx={{ mb: 4 }} />

      <Paper variant="outlined" sx={{ p: 3, display: 'flex', gap: 2, alignItems: 'flex-start' }}>
        <EmailIcon color="secondary" sx={{ mt: 0.5, flexShrink: 0 }} />
        <Box>
          <Typography variant="subtitle1" fontWeight={700} gutterBottom>Email</Typography>
          <Typography color="text.secondary" variant="body2" mb={1}>
            For general inquiries:
          </Typography>
          <Link href="mailto:top8er.app@gmail.com" color="secondary" variant="body1">
            top8er.app@gmail.com
          </Link>
        </Box>
      </Paper>

    </Box>
  );
}

export default ContactPage;

import { Box, Typography, Divider, Paper } from '@mui/material';

interface Section {
  title: string;
  body: string[];
}

const SECTIONS: Section[] = [
  {
    title: 'No account required',
    body: [
      'Top8er does not require you to create an account or provide any personal information to use the service.',
    ],
  },
  {
    title: 'Data you enter',
    body: [
      'Player names, tags, and other data you type into the form are sent to our server solely to generate the graphic image. This data is not stored, logged, or associated with any identifier.',
      'Images uploaded for character art or logos are processed in your browser and transmitted only to the generation endpoint. They are not retained after the request completes.',
    ],
  },
  {
    title: 'Tournament URL imports',
    body: [
      'When you use the "Load from tournament URL" feature, Top8er queries the corresponding third-party API (start.gg, Challonge, Tonamel, or ParryGG) on your behalf. Only public tournament data is fetched. Top8er does not store your tournament URL or the retrieved data.',
    ],
  },
  {
    title: 'Cookies and tracking',
    body: [
      'Top8er does not use tracking cookies or third-party analytics. No advertising networks or data brokers receive information about your visit.',
    ],
  },
  {
    title: 'Third-party services',
    body: [
      'This site is hosted on standard web infrastructure. Standard server logs (IP address, request path, timestamp) may be retained by the hosting provider for security and operational purposes, subject to their own privacy policies.',
    ],
  },
  {
    title: 'Changes to this policy',
    body: [
      'This privacy policy may be updated from time to time. Continued use of the service after changes constitutes acceptance of the revised policy.',
    ],
  },
];

function PrivacyPage() {
  return (
    <Box sx={{ py: 4, maxWidth: 780, mx: 'auto' }}>

      <Box sx={{ mb: 4 }}>
        <Typography variant="overline" color="secondary" letterSpacing={2}>Legal</Typography>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          Privacy Policy
        </Typography>
        <Typography color="text.secondary">
          Top8er is a passion project built for the competitive gaming community.
          We collect as little data as possible — here's exactly what that means.
        </Typography>
      </Box>

      <Divider sx={{ mb: 4 }} />

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {SECTIONS.map((section, i) => (
          <Paper key={i} variant="outlined" sx={{ p: 2.5 }}>
            <Typography variant="subtitle1" fontWeight={700} mb={1}>
              {section.title}
            </Typography>
            {section.body.map((paragraph, j) => (
              <Typography key={j} color="text.secondary" variant="body2" mb={j < section.body.length - 1 ? 1 : 0}>
                {paragraph}
              </Typography>
            ))}
          </Paper>
        ))}
      </Box>

      <Typography variant="caption" color="text.disabled" display="block" mt={4}>
        Last updated: March 2025
      </Typography>

    </Box>
  );
}

export default PrivacyPage;

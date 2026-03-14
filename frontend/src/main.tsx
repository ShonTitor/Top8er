import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Base from './Base';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import CssBaseline from '@mui/material/CssBaseline';
import TemplateForm from './TemplateForm';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import PrivacyPage from './pages/PrivacyPage';
import SpecialThanksPage from './pages/SpecialThanksPage';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/static/beta/" element={<Base />}>
            <Route index element={<HomePage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="privacy" element={<PrivacyPage />} />
            <Route path="special-thanks" element={<SpecialThanksPage />} />
            <Route path="template/:template/" element={<TemplateForm />} />
            <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
          </Route>
          <Route path="/beta/" element={<Base />}>
            <Route index element={<HomePage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="privacy" element={<PrivacyPage />} />
            <Route path="special-thanks" element={<SpecialThanksPage />} />
            <Route path="template/:template" element={<TemplateForm />} />
            <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);

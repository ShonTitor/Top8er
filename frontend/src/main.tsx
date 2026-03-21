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
import ContactPage from './pages/ContactPage';
import BlogPage from './pages/BlogPage';
import BlogPostPage from './pages/BlogPostPage';
import BlogCategoryPage from './pages/BlogCategoryPage';
import BlogAuthorPage from './pages/BlogAuthorPage';
import ErrorBoundary from './ErrorBoundary';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
      <BrowserRouter basename="/beta">
        <Routes>
          <Route path="/" element={<Base />}>
            <Route index element={<HomePage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="privacy" element={<PrivacyPage />} />
            <Route path="special-thanks" element={<SpecialThanksPage />} />
            <Route path="contact" element={<ContactPage />} />
            <Route path="blog" element={<BlogPage />} />
            <Route path="blog/category/:slug" element={<BlogCategoryPage />} />
            <Route path="blog/author/:username" element={<BlogAuthorPage />} />
            <Route path="blog/:slug" element={<BlogPostPage />} />
            <Route path="template/:template" element={<TemplateForm />} />
            <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
      </ErrorBoundary>
    </ThemeProvider>
  </React.StrictMode>
);

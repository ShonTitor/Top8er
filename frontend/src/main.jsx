import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Base from './Base'
import Dog from './Dog'
import TestAPI from './TestAPI'
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import CssBaseline from '@mui/material/CssBaseline';
import TemplateForm from './TemplateForm';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
    <CssBaseline />
    <BrowserRouter>
      <Routes>
        <Route path="/static/beta/" element={<Base />}>
          <Route path="test_api/" element={<TestAPI />} />
          <Route path="template/:template/" element={<TemplateForm />} />
          <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
        </Route>
        <Route path="/beta/" element={<Base />}>
          <Route path="test_api" element={<TestAPI />} />
          <Route path="template/:template" element={<TemplateForm />} />
          <Route path="template/:template/game/:gameName" element={<TemplateForm />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>,
)

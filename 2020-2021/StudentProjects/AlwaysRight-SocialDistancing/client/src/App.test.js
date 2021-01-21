import React from 'react';
import ReactDOM from 'react-dom';
import { render, screen } from '@testing-library/react';

import App from './App';

describe('Main Page suite', () => {
  // Check that the component renders properly and
  // we have no crashes
  test('render App component', () => {
    render(<App />);
  });

  // Check that members list is shown
  test('check members list', () => {
    render(<App />);

    screen.getByText('Berciu Liviu');
    screen.getByText('Cotrau Andreea');
    screen.getByText('Tamas Florin');
    screen.getByText('Ungur Maria');
  })

  test('check video element', () => {
    render(<App />);
    screen.getByText(/Play Video/);
  })

  test('check nav bar', () => {
    render(<App />);

    screen.getByRole("navigation");
    screen.getByText("Home");
    screen.getByText("Surveillance");
    screen.getByText("About Us");
  })
});
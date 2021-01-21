import React from 'react';
import CamTable from './CamTable.js';
import { render, screen } from '@testing-library/react';
import { HashRouter as Router, Route } from 'react-router-dom';

describe('CamTable suite', () => {
    // Check that the component renders properly and
    // we have no crashes
    test('render CamTable component', () => {
        render(<Router><CamTable /></Router>);
    });
});
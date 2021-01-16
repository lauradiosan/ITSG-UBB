import React from 'react';
import ReactDOM from 'react-dom';
import { render, screen } from '@testing-library/react';

import AboutUs from './AboutUs';

describe('AboutUs suite', () => {
    // Check that the component renders properly and
    // we have no crashes
    test('render AboutUs component', () => {
        render(<AboutUs />);
    });
});
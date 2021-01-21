import React from 'react';
import ReactDOM from 'react-dom';
import { render, screen } from '@testing-library/react';

import PageLogo from './PageLogo';

describe('PageLogo suite', () => {
    // Check that the component renders properly and
    // we have no crashes
    test('render PageLogo component', () => {
        render(<PageLogo />);
    });
});
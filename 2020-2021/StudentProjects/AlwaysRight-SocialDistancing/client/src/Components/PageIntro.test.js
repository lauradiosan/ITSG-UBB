import React from 'react';
import ReactDOM from 'react-dom';
import { render, screen } from '@testing-library/react';

import PageIntro from './PageIntro';

describe('PageIntro suite', () => {
    // Check that the component renders properly and
    // we have no crashes
    test('render PageIntro component', () => {
        render(<PageIntro />);
    });
});
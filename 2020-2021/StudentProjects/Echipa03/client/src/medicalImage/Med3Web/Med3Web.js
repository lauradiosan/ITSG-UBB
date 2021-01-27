/**
 * @fileOverview Main Med3Web component
 * @author Epam
 * @version 1.0.0
 */


// ********************************************************
// Imports
// ********************************************************

import React from 'react';
import { connect } from 'react-redux';

import UiApp from './ui/UiApp';

import './Med3Web.css';



// ********************************************************
// Const
// ********************************************************

// ********************************************************
// Class
// ********************************************************

/**
 * Class Med3Web implements all application functionality. This is root class.
 */
class Med3Web extends React.Component {
  /**
   * Main component render func callback
   */
  render() {
    const jsxRender = <UiApp />;
    return jsxRender;
  } // end render
} // end class

// export default Med3Web;
export default connect(store => store)(Med3Web);

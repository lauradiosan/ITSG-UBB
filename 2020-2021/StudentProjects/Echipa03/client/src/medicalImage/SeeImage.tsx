import React from "react";
import Med3Web from "./Med3Web/Med3Web";
import {Provider} from 'react-redux'
import {createStore} from "redux";
import rootReducer from './Med3Web/store/Store';

const SeeImage = () => {

    const store = createStore(rootReducer);

    return (
        <Provider store={store}>
            See the medical image(s) below:
            <Med3Web/>
        </Provider>
    );
}

export default SeeImage;
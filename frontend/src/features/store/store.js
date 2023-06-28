import { configureStore, combineReducers, compose, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

import profile from '../reducers/profile';

const rootReducer = combineReducers({
  user: profile
});

const configureStore = () => {
  return configureStore(
    rootReducer,
    compose(applyMiddleware(thunk))
  );
};

export default configureStore;
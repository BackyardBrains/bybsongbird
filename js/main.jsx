import React from 'react';
import ReactDOM from 'react-dom';
import Sample from './Sample';
import allSamples from './allSamples';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

// render starts with a router, each route matches an url
ReactDOM.render(
  (
    <Router>
      <Switch>
        <Route path="/" component={index_samples}/>
        <Route path="/allsamples" component={all_samples}/>
      </Switch>
    </Router>
  ),
  document.getElementById("reactEntry"),);

// render the react components for displaying sample birds on home page
function index_samples(){
  return (<Sample url="/api/index"/>);
}


// renders the all samples' page react components
function all_samples(){
  return (<allSamples url="/api/allsamples"/>);
}
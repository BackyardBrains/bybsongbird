import React from 'react';
import ReactDOM from 'react-dom';
import Sample from './Sample';
import AllSamples from './AllSamples';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

// render starts with a router, each route matches an url
ReactDOM.render(
  (
    <Router>
      <Switch>
        <Route exact path="/" component={index_samples}/>
        <Route exact path="/allsamples/" component={All_samples}/>
      </Switch>
    </Router>
  ),
  document.getElementById("reactEntry"),);

// render the react components for displaying sample birds on home page
function index_samples(){
  return (<Sample url="/api/index"/>);
}


// renders the all samples' page react components
function All_samples(){
  return (<Sample url="/api/allsamples"/>);
}
/* eslint-disable no-unused-vars */
import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Sample from './sample';

const TYPE_BACK_FORWARD = 2;

class InfScroll extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: [],
    };
    this.fetchMoreData = this.fetchMoreData.bind(this);
  }


  componentDidMount() {
    /* Call REST API to get 10 posts */
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (PerformanceNavigation.type === TYPE_BACK_FORWARD) {
          this.setState(history.state);
        } else {
          this.setState({
            results: data.results,
            next: data.next === undefined ? '' : data.next,
          });
          history.replaceState(this.state, '');
        }
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }


  fetchMoreData(nextUrl) {
    // console.log(this.state.next);
    if (nextUrl === undefined || nextUrl === '') {
      return false;
    }
    fetch(nextUrl, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log(this.state.results); // eslint-disable-line no-console
        if (PerformanceNavigation.type === TYPE_BACK_FORWARD) {
          this.setState(history.state);
        } else {
          this.setState({
            results: this.state.results.concat(data.results),
            next: data.next,
          });
          history.replaceState(this.state, '');
        }
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
    return true;
  }

  render() {
    // this.state.results.map(post => console.log(post.postid));
    // console.log(this.fetchMoreData);
    return (
      <InfiniteScroll
        dataLength={this.state.results.length}
        next={() => this.fetchMoreData(this.state.next)}
        hasMore
        loader={<h4>Loading...</h4>}
      >
        {this.state.results.map(post =>
          (
            <Sample key={post.postid.toString()} url={post.url} />
          ))}
      </InfiniteScroll>

    ); // return()
  }
}

InfScroll.propTypes = {
  url: PropTypes.string.isRequired,
};

export default InfScroll;

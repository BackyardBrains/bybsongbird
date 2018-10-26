import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes a like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { num_likes: 0, logname_likes_this: false };
    // !!!! Must have this binding call for the click to work
    this.clickLike = this.clickLike.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          num_likes: data.likes_count,
          logname_likes_this: data.logname_likes_this,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  // Handles the action of clicking the like button
  clickLike(event) {
    event.preventDefault();
    // Call REST API to post or delete a like
    fetch(this.props.url, {
      method: this.state.logname_likes_this ? 'DELETE' : 'POST',
      credentials: 'same-origin',
    })
      .then((response) => {
        // Handle error
        if (!response.ok) throw Error(response.statusText);
      })
      .then(() => {
        this.setState(prevState => ({
          num_likes: prevState.logname_likes_this ?
            prevState.num_likes - 1 : prevState.num_likes + 1,
          logname_likes_this: !prevState.logname_likes_this,
        }));
      });
  }


  render() {
    // Render number of likes
    return (
      <div className="likes">
        <button id="like-unlike-button" onClick={this.clickLike}>
          {this.state.logname_likes_this ? 'Unlike' : 'Like'}
        </button>
        <p>{this.state.num_likes} like{this.state.num_likes !== 1 ? 's' : ''}</p>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;

import React from 'react';
import PropTypes from 'prop-types';
import Likes from './likes';
import Comments from './comments';

class Posts extends React.Component {
  /* Display posts
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state+
    super(props);
    this.state = {
      age: 1,
      owner: 'unknown',
      owner_img_url: '/',
      owner_show_url: '/u/awdeorio/',
      post_show_url: ' ',
    };
  }

  componentDidMount() {
    // Call REST API to get a post
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // alert(data.results[1].url);
        this.setState({
          age: data.age,
          owner: data.owner,
          img_url: data.img_url,
          owner_img_url: data.owner_img_url,
          owner_show_url: data.owner_show_url,
          post_show_url: data.post_show_url,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  render() {
    const like = 'likes/';
    const comments = 'comments/';
    // Render post
    return (
      <li className="post">
        <ul className="postlayout">
          <li>
            <a href={this.state.owner_show_url}>
              <img className="avatar" src={this.state.owner_img_url} alt="avatar" />
            </a>
            <span className="postusername">{this.state.owner}</span>
            <span className="posttime">
              <a href={this.state.post_show_url}>{this.state.age}</a>
            </span>
          </li>
          <li>
            <img className="postimg" src={this.state.img_url} alt="postimg" />
          </li>
          <Likes url={this.props.url + like} />
          <Comments url={this.props.url + comments} />
        </ul>
      </li>
    );
  }
}

Posts.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Posts;

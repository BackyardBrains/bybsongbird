import React, {Component} from "react";
import {View, Text, Image, ScrollView} from "react-native";
import CardSection from "./common/CardSection";
import Button from "./common/Button"
import axios from 'axios';

const Sound = require('react-native-sound')
const s = new Sound('http://songbird.backyardbrains.com/api', undefined, (e) => {
    if (e) {
      console.log(e);
    }
});

class MainPage extends Component {
  state = {playSound: false, text: ""};

  componentWillMount() {
    //axios.get('http://songbird.backyardbrains.com/api')
    //.then(response => this.setState({ text: response.data }));
  }

  playSound() {
    if(this.state.playSound == true)
    {
      s.stop();
      console.log("stopping")
    }
    if(this.state.playSound == false)
    {
      s.play();
      console.log("playing")
    }
    this.setState({playSound: !this.state.playSound})
  }

  render()
  {
    const { imageStyle, viewStyle, textStyle, headerStyle } = styles
    return(
      <ScrollView>
        <CardSection>
          <Image
            source={require('../images/byblogo.jpg')}
            style={headerStyle}
          />
        </CardSection>
        <CardSection>
          <Text style={textStyle}>
            {"The Backyard Brains Wildlife recording system is designed to continuosly listen and upload the sounds of it's environment, as well as classify 8 different species of bird!"}
          </Text>
        </CardSection>
        <CardSection>
          <Button onPress={this.playSound.bind(this)}>
            {"Listen to what's recording right now!"}
          </Button>
        </CardSection>

        <CardSection>
          <Image
            source={require("../images/device.jpg")}
            style={imageStyle}
          />
        </CardSection>
        <View style={viewStyle}>
          <Text style={textStyle}> The Recording Device </Text>
        </View>

      </ScrollView>
    );
    }
}

const styles = {
  viewStyle: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerStyle: {
    height: 50,
    flex: 1,
    width: undefined
  },
  textStyle: {
    fontSize: 18,
    flex:1,
    paddingLeft: 5
  },
  imageStyle: {
    height: 260,
    flex: 1,
    width: undefined
  },
}

export default MainPage;

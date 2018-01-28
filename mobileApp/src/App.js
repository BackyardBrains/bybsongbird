import React, {Component} from "react";
import {View, Text, Image} from "react-native";
import CardSection from "./components/common/CardSection";
import Button from "./components/common/Button"

class App extends Component{
  playSound() {
    const Sound = require('react-native-sound')
    const s = new Sound('birdinrain.mp3', Sound.MAIN_BUNDLE, (e) => {
            if (e) {
              console.log('error', e);
            } else {
              s.setSpeed(1);
              console.log('duration', s.getDuration());
              s.play(() => s.release()); // Release when it's done so we're not using up resources
            }
          });
    console.log("here");
  }

  render()
  {
    const { imageStyle, viewStyle, textStyle } = styles
    return(
      <View>
        <CardSection>
          <Image
            source={require('./images/byblogo.jpg')}
            style={imageStyle}
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
      </View>
    );
  }
}

const styles = {
  viewStyle: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageStyle: {
    height: 50,
    flex: 1,
    width: undefined
  },
  textStyle: {
    fontSize: 18
  }
}

export default App;

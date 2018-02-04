import React, {Component} from "react";
import {View, Text, Image, ScrollView} from "react-native";
import CardSection from "./common/CardSection";
import Button from "./common/Button"

class Upload extends Component {
  render()
  {
    const { textStyle, viewStyle } = styles
    return(
        <CardSection>
          <Text style={textStyle}> Upload your own bird sounds! </Text>
          <Button>
            upload
          </Button>
        </CardSection>
    );
    }
}

const styles = {
  textStyle: {
    fontSize: 18,
    flex:1,
    paddingLeft: 5
  },
  viewStyle: {
    justifyContent: 'center',
    alignItems: 'center',
  }
}

export default Upload;

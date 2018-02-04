import React, {Component} from "react";
import {View, Text, Image, ScrollView} from "react-native";
import CardSection from "./components/common/CardSection";
import MainPage from "./components/MainPage";
import Upload from "./components/Upload";
import Swiper from 'react-native-swiper';


class App extends Component{
  render() {
    return(
      <Swiper loop={false} showButtons={true}>
        <MainPage/>
        <Upload/>
      </Swiper>
    );
  }
}

export default App;

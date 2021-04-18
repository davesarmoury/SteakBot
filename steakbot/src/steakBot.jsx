import React, { Component } from 'react';
import Carousel from 'react-bootstrap/Carousel'
import ButtonGroup from 'react-bootstrap/ButtonGroup'
import Button from 'react-bootstrap/Button'

class SteakBot extends Component {
  state = {
    meat:0,
    cook:-1
  }

  handleCook = (val) => {
    this.setState({ cook: val });
  };

  handleMeat = (event) => {
    this.setState({ meat: event });
  };

  goSteakBot = () => {
    var fetch_url = "http://192.168.2.104:5000/go";
    fetch_url = fetch_url.concat("?meat=" + this.state.meat);
    fetch_url = fetch_url.concat("&cook=" + this.state.cook);
    fetch(fetch_url);
  };

  render() {
    return (
      <React.Fragment>
        <Carousel interval={null} onSlid={this.handleMeat}>
          <Carousel.Item>
            <img
              src="images/TBone.png"
              alt="T-bone"
            />
            <Carousel.Caption>
              <h3>T-Bone</h3>
            </Carousel.Caption>
          </Carousel.Item>
          <Carousel.Item>
            <img
              src="images/Strip.png"
              alt="New York Strip"
            />

            <Carousel.Caption>
              <h3>New York Strip</h3>
            </Carousel.Caption>
          </Carousel.Item>
          <Carousel.Item>
            <img
              src="images/Ribeye.png"
              alt="Rib-Eye"
            />

            <Carousel.Caption>
              <h3>Rib-Eye</h3>
            </Carousel.Caption>
          </Carousel.Item>
        </Carousel>

        <ButtonGroup size="lg">
          <Button variant="secondary" onClick={() => this.handleCook(0)}>Rare</Button>
          <Button variant="secondary" onClick={() => this.handleCook(1)}>Medium Rare</Button>
          <Button variant="secondary" onClick={() => this.handleCook(2)}>Medium</Button>
          <Button variant="secondary" onClick={() => this.handleCook(3)}>Medium Well</Button>
          <Button variant="secondary" onClick={() => this.handleCook(4)}>Well</Button>
        </ButtonGroup>

        <Button variant="danger" size="lg">Perfection!</Button>
      </React.Fragment>
     );
  }
}

export default SteakBot;

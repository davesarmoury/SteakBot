import './App.css';

import Carousel from 'react-bootstrap/Carousel'
import ButtonGroup from 'react-bootstrap/ButtonGroup'
import Button from 'react-bootstrap/Button'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Carousel interval={null}>
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
          <Button variant="secondary">Rare</Button>
          <Button variant="secondary">Medium Rare</Button>
          <Button variant="secondary">Medium</Button>
          <Button variant="secondary">Medium Well</Button>
          <Button variant="secondary">Well</Button>
        </ButtonGroup>

        <Button variant="danger" size="lg">Perfection!</Button>

      </header>
    </div>
  );
}

export default App;

import './App.css';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Container>
          <h1 className="mb-4">Make Your Confession Below</h1> {/* Title */}
          <Form>
            <Form.Group as={Row} controlId="inputConfession" className="mb-3">
              <Form.Label column sm={2}>Enter Confession:</Form.Label>
              <Col sm={10}>
                <Form.Control as="textarea" rows={5} required />
              </Col>
            </Form.Group>

            <Form.Group as={Row} controlId="city">
              <Form.Label column sm={2}>Enter city name:</Form.Label>
              <Col sm={10}>
                <Form.Control type="text" placeholder="Location" required />
              </Col>
            </Form.Group>

            <Form.Group as={Row} className="mb-3">
              <Col sm={{ span: 10, offset: 2 }}>
                <Button type="submit" variant="primary">Confess</Button>
              </Col>
            </Form.Group>
          </Form>
        </Container>
      </header>
    </div>
  );
}

export default App;

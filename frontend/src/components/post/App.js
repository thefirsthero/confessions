import './App.css';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import axios from 'axios'; // Import axios

function App() {
  const [confession, setConfession] = useState('');
  const [city, setCity] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Define the API endpoint URL based on environment
    const apiUrl = process.env.NODE_ENV === 'development'
      ? 'http://127.0.0.1:8000/addConfession'
      : '/production-api-url'; // Replace with your production API URL

    try {
      const response = await axios.post(apiUrl, {
        confession,
        city,
      });
      
      // Handle success, reset form, display a message, etc.
      console.log('Submission successful', response);
      setConfession('');
      setCity('');
    } catch (error) {
      // Handle errors, display error message, etc.
      console.error('Error submitting form', error);
    }
  };

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

import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <form>
          <div class="form-group row">
            <label for="inputConfession" class="col-sm-2 col-form-label">Enter Confession:</label>
            <div class="col-sm-10">
              <textarea class="form-control" id="inputConfession" rows="5" required></textarea>
            </div>
          </div>
          <div class="form-group row">
            <label for="city" class="col-sm-2 col-form-label">Enter city name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="city" placeholder="Location" required />
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Confess</button>
            </div>
          </div>
        </form>
      </header>
    </div>
  );
}

export default App;

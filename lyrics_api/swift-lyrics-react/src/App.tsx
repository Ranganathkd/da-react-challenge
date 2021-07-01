import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Button, Table} from "reactstrap";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Find your favorite!
        </p>
        <Table>
         <thead>
            <tr>
              <th></th>
              <th>Lyrics</th>
              <th>Song</th>
              <th>Album</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
            <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>"Their parties were tasteful, if a little loud"</td>
                  <td>The Last Great American Dynasty</td>
                  <td>Folklore</td>
                  <td>Edit</td>
                  <td>Delete</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>"In my feelings more than Drake"</td>
                  <td>I Forgot That You Existed</td>
                  <td>Lover</td>
                  <td>Edit</td>
                  <td>Delete</td>
                </tr>
            </tbody>
        </Table>
      </header>
    </div>
  );
}

export default App;

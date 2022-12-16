import React, { Component } from 'react';

import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import Parking1 from "./pages/Parking1";
import Parking2 from "./pages/Parking2";

function App() {


  return (
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path={"/"} element={<Home/>}/>
            <Route path={"/parking/1"} element={<Parking1/>}/>
              <Route path={"/parking/2"} element={<Parking2/>}/>
          </Routes>
        </BrowserRouter>
      </div>
  );
}

export default App;

import Nav from "../components/Nav";
import React, {Component} from "react";

import mqtt from 'mqtt'

const Home = () => {

    return(
        <>
            <Nav/>
            <div>
                <p>Sélectionner la place que vous avez choisi</p>
            </div>
            <div className="cards-list">
                <a href={"/parking/1"}>
                    <div className="card 1">
                        <div className="card_image">
                            <img
                                src="https://media.istockphoto.com/id/1083622428/vector/car-parking-icon.jpg?s=612x612&w=0&k=20&c=Z6VydNYDHrBq6gujhSuC6eIaCXQn_eMHNBFf8Co0ul4="/>
                        </div>
                        <div className="card_title title-black">
                            <p>Parking place n°1</p>
                        </div>
                    </div>
                </a>

                <a href={"/parking/2"}>
                    <div className="card 2">
                        <div className="card_image">
                            <img
                                src="https://media.istockphoto.com/id/1083622428/vector/car-parking-icon.jpg?s=612x612&w=0&k=20&c=Z6VydNYDHrBq6gujhSuC6eIaCXQn_eMHNBFf8Co0ul4="/>
                        </div>
                        <div className="card_title title-black">
                            <p>Parking place n°2</p>
                        </div>
                    </div>
                </a>
            </div>
        </>
    )
}

export default Home;
import React, {useEffect, useState} from "react";
import axios from "axios";
import Nav from "../components/Nav"
import {useNavigate} from "react-router-dom";

const Parking1 = () => {
    const [listParking, setListParking] = useState(null)
    const [data, setData] = useState(null)
    const [name, setName] = useState(null)

    let navigate = useNavigate();
    const getListParking = async () =>{
        try{
            const response = await axios.get('http://localhost:4000/parking1')
            setListParking(response.data)
        }catch (e){
            console.log(e)
        }
    }

    const check = async () =>{
        try{
            if(lastPark.status === 1){
                const response = await axios.get('http://localhost:4000/check',{
                    lastPark
                })
                console.log(response, 'test')
            }
        }catch (e){
            console.log(e)
        }
    }

    useEffect(() => {
        if(lastPark){
            check()
        }
    }, [])
    useEffect(() => {
        getListParking()

    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault()
        try{
            const response = await axios.put("http://localhost:4000/name",{
                name, parkId: lastPark.park_id
            })
            const success = response.status === 200 || 201
            if(success) navigate('/parking/1')
        }catch (e) {
            console.log(e)
        }
    }

    const lastPark = listParking ? listParking.slice(-1).pop() : null
    console.log(lastPark)
    return(
        <>
            <Nav/>

            <div className="cards-list">
                <a>
                    <div className="card 1">
                        <div className="card_image">
                            <img
                                src="https://media.istockphoto.com/id/1083622428/vector/car-parking-icon.jpg?s=612x612&w=0&k=20&c=Z6VydNYDHrBq6gujhSuC6eIaCXQn_eMHNBFf8Co0ul4="/>
                        </div>
                        <div className="card_title title-black">
                            { lastPark && lastPark.status === 1 && <p>Place Prise</p>}
                            { lastPark && lastPark.status === 0 && <p>Place Libre</p>}
                        </div>
                    </div>
                </a>
            </div>
            <table id="exampl">
                <thead className="TableHead">
                <tr>
                    <th>Status</th>
                    <th>date</th>
                    <th>Temps</th>
                    <th>Nom</th>
                    <th>Amendes</th>
                </tr>
                </thead>
                <tbody>
                { listParking && listParking.map((parking, index) =>
                    <tr>
                        {parking.status === 1 &&  <td>Pris</td>}
                        {parking.status === 0 &&  <td>Libre</td>}
                        <td>{parking.date}</td>
                        <td>{parking.time}</td>
                        {parking.name && <td>{parking.name}</td>}
                        {parking.amendes && <td>{parking.amendes}</td>}
                    </tr>
                )}

                </tbody>
            </table>
            <form onSubmit={handleSubmit}>
                { lastPark && lastPark.status === 1 && !lastPark.name &&
                    <>
                        <input id="name" name="name" required={true} placeholder="Thomas" onChange={(e) => setName(e.target.value)}/>
                        <input id="status" name="status" value={lastPark.status} readOnly/>
                        <input id="date" name="date" value={lastPark.date} readOnly/>
                        <input id="time" name="time" value={lastPark.time} readOnly/>
                        <input type="submit"/>
                    </>
                }
            </form>
        </>
    )
}

export default Parking1
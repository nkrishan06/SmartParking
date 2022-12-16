const express = require('express');
const { MongoClient } = require('mongodb')
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');
const app = express();
const uri  = "mongodb+srv://krishan:mypassword@cluster0.fm6vpot.mongodb.net/?retryWrites=true&w=majority"
app.use(cors())
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use('/', express.static('public'));


// MQTT
const mqtt = require('mqtt')
const { v4 : uuidv4 } = require('uuid')
const {response} = require("express");
const client  = mqtt.connect('mqtt://broker.emqx.io')
const client1 = mqtt.connect('mqtt://broker.emqx.io')

client.on('connect',  function () {
    client.subscribe('pk_ps/uds/sciences/1', function (err) {
        console.log('connected')
    })
    client.on('message', async function (topic, message) {
        // message is Buffer
        const mongoClient = new MongoClient(uri);
        const data = JSON.parse(message.toString());
        const time = data.time;
        const status = data.status;
        const id = data.id;
        const date = data.date;
        const generatedUserId = uuidv4();
        try{
            await mongoClient.connect()
            const database = mongoClient.db('smart-parking')
            const parking = database.collection('parking1')

            const data = {
                park_id: generatedUserId,
                status: status,
                id: id,
                date: date,
                time: time
            }

            await parking.insertOne(data)
        }catch (e) {
            console.log(e)
        }

    });
})

client1.on('connect',  function () {
    client1.subscribe('pk_ps/uds/sciences/2', function (err) {
        console.log('connected')
    })
    client1.on('message', async function (topic, message) {
        // message is Buffer
        const mongoClient = new MongoClient(uri);
        const data = JSON.parse(message.toString());
        const time = data.time;
        const status = data.status;
        const id = data.id;
        const date = data.date;
        const generatedUserId = uuidv4();
        try{
            await mongoClient.connect()
            const database = mongoClient.db('smart-parking')
            const parking = database.collection('parking2')

            const data = {
                park_id: generatedUserId,
                status: status,
                id: id,
                date: date,
                time: time
            }

            await parking.insertOne(data)
        }catch (e) {
            console.log(e)
        }finally {
            await mongoClient.close()
        }

    });
})

// * END MQTT



app.get('/parking1', async (req, res) => {
    const mongoClient = new MongoClient(uri);
    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const parking = database.collection('parking1')

        const data = await parking.find().toArray()
        res.send(data)
    }catch (e) {
        console.log(e)
    }finally {
        await mongoClient.close()
    }
})



app.put('/name', async (req,res) => {
    const mongoClient = new MongoClient(uri)
    const { name, parkId } = req.body
    console.log(parkId)
    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const users = database.collection('parking1')

        const query = {park_id: parkId}
        const options = {upsert: true}

        const updateDocument = {
            $set: {name: name}
        }
        const user = await users.updateOne(query, updateDocument);
        res.send(user)
    }catch (e) {

    }finally {
        await mongoClient.close()
    }
})


app.get('/parking2', async (req, res) => {
    const mongoClient = new MongoClient(uri);
    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const parking = database.collection('parking2')

        const data = await parking.find().toArray()
        res.send(data)
    }catch (e) {
        console.log(e)
    }finally {
        await mongoClient.close()
    }
})



app.put('/name2', async (req,res) => {
    const mongoClient = new MongoClient(uri)
    const { name, parkId } = req.body
    console.log(parkId)
    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const users = database.collection('parking1')

        const query = {park_id: parkId}
        const options = {upsert: true}

        const updateDocument = {
            $set: {name: name}
        }
        const user = await users.updateOne(query, updateDocument);
        res.send(user)
    }catch (e) {

    }finally {
        await mongoClient.close()
    }
})


async function amendes(){

    const mongoClient = new MongoClient(uri);

    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const parking = database.collection('parking1')

        const data = await parking.find().toArray()
        const lastPark = data.slice(-1).pop()
        const lastParkDate = lastPark.date.replace(/\//g, "-");
        const lastParkTime = new Date(lastParkDate +'T' + lastPark.time+'.000Z')
        const dateNow = new Date()

        const diff = (dateNow.getTime() - lastParkTime.getTime()) / 60000
        const amendes = "25$"
        console.log(diff)
        if(diff > 2 && lastPark.status === 1 && !lastPark.amendes){
            console.log(lastPark.park_id)
            const query = {park_id: lastPark.park_id}
            const updateDocument = {
                $set: { amendes: amendes}
            }
            await parking.updateOne(query, updateDocument);
        }
    }catch (e) {
        console.log(e)
    }finally {
        await mongoClient.close()
    }
}

async function amendes2(){

    const mongoClient = new MongoClient(uri);

    try {
        await mongoClient.connect()
        const database = mongoClient.db('smart-parking')
        const parking = database.collection('parking2')

        const data = await parking.find().toArray()
        const lastPark2 = data.slice(-1).pop()
        const lastParkDate = lastPark2.date.replace(/\//g, "-");
        const lastParkTime = new Date(lastParkDate +'T' + lastPark2.time+'.000Z')
        const dateNow = new Date()

        const diff = (dateNow.getTime() - lastParkTime.getTime()) / 60000
        const amendes = "25$"
        console.log(diff)
        if(diff > 2 && lastPark2.status === 1 && !lastPark2.amendes){
            console.log(lastPark2.park_id)
            const query = {park_id: lastPark2.park_id}
            const updateDocument = {
                $set: { amendes: amendes}
            }
            await parking.updateOne(query, updateDocument);
        }
    }catch (e) {
        console.log(e)
    }finally {
        await mongoClient.close()
    }
}

setInterval(amendes, 120000) //Toutes les deux minutes, on verifie si on met une amende
setInterval(amendes2, 120000)
module.exports = app;

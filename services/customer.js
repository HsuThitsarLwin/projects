const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;

const app = express();
app.use(cors());
app.use(bodyParser.json());

// For Windows
// const sequelize = new Sequelize(process.env.db_name, process.env.username, process.env.password, {host: process.env.host, dialect: 'mysql'});

// For Mac
const sequelize = new Sequelize(process.env.db_name, process.env.username, process.env.password, {host: process.env.host, port: process.env.port, dialect: 'mysql'});

// Define Customer Model
const Customer = sequelize.define(
  'customer', {
    cid: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
    name: { type: Sequelize.STRING(256), allowNull: false },
    email_addr: { type: Sequelize.STRING(256), allowNull: false },
    dateOfBirth: { type: Sequelize.DATEONLY, allowNull: false },
    balancePoints: { type: Sequelize.INTEGER, allowNull: false },
    tier: { type: Sequelize.STRING(256), allowNull: false }
}, {
  timestamps: false,
  tableName: 'customer'
});

// Retrieving all customer data
app.get('/customer', async (req, res) => {
  try {
    const customerlist = await Customer.findAll();
    if (customerlist.length > 0) {
      res.status(200).json({
        code: 200,
        data: {
          customer: customerlist
        }
      });
    } else {
      res.status(404).json({
        code: 404,
        message: 'There are no customers.'
      });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({
      code: 500,
      message: 'Internal Server Error'
    });
  }
});

// Retrieving specific customer data
app.get('/customer/:cid', async (req, res) => {
  const { cid } = req.params;
  try {
      const customer = await Customer.findOne({ where: { cid } });
      if (customer) {
          res.status(200).json({
              code: 200,
              data: customer.toJSON()
          });
      } else {
          res.status(404).json({
              code: 404,
              message: "Customer not found."
          });
      }
  } catch (error) {
      console.log(error);
      res.status(500).json({
          code: 500,
          message: "An error occurred while retrieving the customer."
      });
  }
});

// Retrieving customer based on tier
app.get('/customer/customer_by_tier/:tier', async (req, res) => {
  const { tier } = req.params;
  try {
      const customers = await Customer.findAll({ where: { tier } });
      if (customers.length) {
          res.status(200).json({
              code: 200,
              data: customers.map(customer => customer.toJSON())
          });
      } else {
          res.status(404).json({
              code: 404,
              message: "No customer in this tier found."
          });
      }
  } catch (error) {
      console.log(error);
      res.status(500).json({
          code: 500,
          message: "An error occurred while retrieving the customers."
      });
  }
});

// Update specific customer balance points
app.put("/customer/:cid", (req, res) => {
  const { cid } = req.params;
  const { balancePoints } = req.body;

  Customer.update({ balancePoints }, { where: { cid } })
    .then(() => {
      return Customer.findByPk(cid);
    })
    .then((customer) => {
      res.json({
        code: 201,
        data: customer,
      });
    })
    .catch(() => {
      res.status(500).json({
        code: 500,
        data: { cid },
        message: "An error occurred while deducting the points.",
      });
    });
});

// Listening to port
const port = process.env.PORT || 5200;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
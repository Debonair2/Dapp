import os
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from brownie import accounts, Contract , network
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb111"
network.connect('rinkeby')
usdcAddress = Contract('0x196540A613F5483366A5672aea95c1dC09aD860C')
defi_contract = Contract('0xc2aAFE8E1363FF2f733d74dDb2f3054EAd9562eD')

account = accounts.add(os.getenv("PRIVATE_KEY"))
accounts.add(os.getenv("PRIVATE_KEY1"))
accounts.add(os.getenv("PRIVATE_KEY2"))

class Form(FlaskForm):
    Faccounts = SelectField('Account' , choices = ['0xB5F909f81259076Dbb86545F4AC93Ca9454d157b',
                                                    '0x6b7aE4e2d3D8492d1164F4820846A22F56513d86',
                                                    '0xF3cbcD528bb67C0EE3fCBE8e160828bF6fdbf92a'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit')
def deposit():
    form = Form()
    AvailableBal = SC_getAccountbal() / 10 ** 18
    DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
    return render_template('deposit.html', form = form, AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/depositButton', methods =['GET', 'POST'])
def depositButton():
    form = Form()
    if request.method == 'POST':
        depositAmount = request.form.get("depositValue", type = int) * (10 ** 18)
        SC_depositBal(depositAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/withdrawButton', methods =['GET', 'POST'])
def withdrawButton():
    form = Form()
    if request.method == 'POST':
        withdrawAmount = request.form.get("withdrawValue", type = int) * (10 ** 18)
        SC_withdrawBal(withdrawAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

def SC_withdrawBal(withdrawAmount):
    defi_contract.withdraw(withdrawAmount, {"from": account})

def SC_getAccountbal():
    balance = usdcAddress.balanceOf(account)
    return balance

def SC_depositBal(depositAmount):
    usdcAddress.approve(defi_contract, depositAmount, {"from": account})
    defi_contract.depositToken(depositAmount, {"from": account})

@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account = accounts.at(currentAccount)
    currentBal = usdcAddress.balanceOf(account) /(10 ** 18)
    stakedBalance = defi_contract.depositBalance(account) / (10 ** 18)
    return jsonify({'response' : currentAccount ,'stakedBalance' : stakedBalance , 'currentBal': currentBal})

@app.route('/FundMe', methods =["GET", "POST"])
def FundMe():
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        FromAddress = accounts.at(FromAddress, force=True)
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type = int)
        usdcAddress.transfer(ToAddress, Amount * 10 ** 18, {"from": FromAddress})
    return render_template('FundMe.html')

if __name__ == "__main__":
    
    app.run()
    network.disconnect()
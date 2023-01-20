from datetime import datetime
import json
from flask import jsonify, make_response, request
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pickle
import codecs

from app import app
from app.vote_counter import VoteCounter
from app.logger import Logger

vc = VoteCounter(datetime(2023, 1, 20, 17, 00))

private_key = RSA.generate(2048)
public_key = private_key.publickey()

private_key_pem = private_key.export_key()
public_key_pem = public_key.export_key()


@app.route("/", methods=["GET"])
def health_check():
    payload = {"message": "Vote counting service", "status": "success"}
    return jsonify(payload), 200, {"Content-Type": "application/json"}


@app.route("/public_key", methods=["GET"])
def public_key():
    bytes_key = pickle.dumps(vc.get_public_key())
    str_public_key = codecs.encode(bytes_key, "base64").decode()
    payload = {"public": str_public_key, "status": "success"}
    return jsonify(payload), 200, {"Content-Type": "application/json"}


@app.route("/results", methods=["GET"])
def results():
    if request.method == "GET":
        logger = Logger()
        success, results = vc.generate_results()
        if not success:
            logger.warning("Unauthorized access detected from " + request.remote_addr)
            logger.warning("Unauthorized access type: " + results)
            payload = {"status": "fail", "message": results}
            return make_response(
                jsonify(payload), 400, {"Content-Type": "application/json"}
            )

        private_key = RSA.import_key(private_key_pem)
        hashed_data = SHA256.new(json.dumps(results).encode())
        signature = pkcs1_15.new(private_key).sign(hashed_data)
        payload = {
            "results": results,
            "signature": signature.hex(),
            "public-key": public_key_pem.decode(),
            "status": "success",
        }
        logger.green("Sent vote results")
        return make_response(
            jsonify(payload), 200, {"Content-Type": "application/json"}
        )

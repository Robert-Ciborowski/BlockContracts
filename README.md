# BlockContracts
## Our mission
We want to make corporate contracts more secure by use of blockchain and machine learning technology.
- _We want contracts to be tamper-proof._ Conditions in paper contracts could be illegally modified after the contracts are signed.
- _We want contracts to be forge-proof._ Every contract should contain proof that its signatures are not fake.
- _We want contracts to be friendly._ When a contract leaves conditions to be ambiguous, the person signing the contract deserves to know.

## How it works
BlockContracts is an application in which you create and sign corporate contracts. When you sign a contract with BlockContracts, you back your signature with a piece of personal information only accessible to you and your country's government (e.g. tax return information). Your information-backed signature is encrypted, then encrypted again along with the contract, and is added to BlockContracts' blockchain network. Every person who signed the contract is given a personal key (in the form of a file) which can read the contract from the blockchain.

#### Proof that your contract is real
You can prove that a signatory signed your contract in court. Courts can be given your personal key to download and unencrypt the contract from the blockchain. Afterwards, courts can verify that the signatory's encrypted signature belongs to them. Only the signatory and the government have access to the information which backs their signature, and thus the government can match this information with the signatory's unique, encrypted signature.

#### Tamper-proof contracts
Any contract signed with Blockcontracts is unmodifiable once signed. This is because Blockcontracts adds an encrypted copy of the contract to a public blockchain running on a network of computers. The contracts stored on the blockchain cannot be modified, and each one of these contracts can be downloaded and unencrypted only by the signatories (by use of their personal keys).

#### Unambiguous contracts
When using Blockcontracts, each contract you are about to sign is pre-read by the program. The contract is scanned for ambiguous conditions with the help of a machine learning algorithm. If the algorithm detects ambiguity, it will alert you.

## How we built it
BlockContracts is powered by a **custom-made Blockchain network**. We originally intended to fork the Bitcoin blockchain, but decided to build a custom solution in Python due to time restrictions. Our blockchain network is backed by SHA256 encryption. We ensure that at least one node on our blockchain is always running by hosting a node on a **DigitalOcean linux server**.

BlockContracts uses a **custom TensorFlow 2 model** to detect ambiguity in contracts. Our model uses text embeddings along with a neural network in order to detect ambiguity in phrases throughout the entire contract. The dataset we used is public domain. With our limited training time, we achieved an accuracy of ~85%  along with desirable precision and recall.

BlockContracts encrypts contract information by use of the **Fernet symmetric encryption API**. Fernet guarantees that a contract encrypted using it cannot be manipulated or read without the personal key of one of the signatories.

BlockContracts' GUI is built using **tkinter**, Python's GUI toolkit. Tkinter powers our clean and simple user experience while keeping our program cross-compatible with all platforms.

## Q&A
- Q: _What kind of information can I use to back my signature?_
- A: Any information which only the signatory and the government have access to can be used. This includes the lines on tax return filings.
- Q: _How do I run BlockContracts?_
- A: If using a unix-based operating system, simply run the run_end_user_app.bash script. Otherwise, run front-end/end_user_app/start_end_user_app.py. Our program can be downloaded from https://github.com/Robert-Ciborowski/BlockContracts.
- Q: _Can someone hack into my contract?_
- A: No! All contracts stored on the BlockContracts blockchain are encrypted by symmetric encryption. Only the signatories can read these contracts. When a contract is unencrypted for reading purposes, the information-backed signatures remain encrypted and can only be verified by the signatory and the government.

## Challenges we ran into
One challenge we ran into was the absence of our fourth member, who was not able to attend this hackathon. This member was to be responsible for our front-end GUI. To overcome this issue, we all participated in the creation of the GUI.

Another challenge we ran into was related to our front-end's connectivity with the blockchain as well as its retrieval of encrypted data. We overcame this challenge by spending more time fixing these issues.

## Accomplishments that we're proud of
- This was our first time implementing blockchain in a project. We read up about blockchain implementations in preparation for the hackathon, but wrote our first line of blockchain code once the hackathon started.
- This was our first time implementing a machine learning algorithm which uses embeddings. We used a tutorial to guide us through the process of adding an embeddings layer to our model.
- This was our first time implementing incredibly high encryption standards into any project. We learned a lot about symmetric encryption throughout this hackathon.

## What's next for BlockContracts
We hope to extend BlockContracts' uses to outside the security of corporate contracts. We believe that the idea of using blockchain for encryption storage can be applied to other fields, such as ownership of personal assets. Stay tuned!

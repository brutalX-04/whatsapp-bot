const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const { Sticker, createSticker, StickerTypes } = require('wa-sticker-formatter');
const { downloadMediaMessage, Mimetype, MessageType  } = require('@whiskeysockets/baileys');
const rmvbg = require('./tools/rmvbg.js');
const sticker = require('./tools/sticker.js');
const cheerio = require('cheerio');
const axios = require('axios');
const pino = require('pino');
const fs = require('fs');
const write = require('fs/promises');


const logger = pino();

async function connectToWhatsapp() {
    const { state, saveCreds } = await useMultiFileAuthState("auth");
    const socket = makeWASocket({
        printQRInTerminal: true,
        browser: ["brutalx", 'Chrome', "1.0.0"],
        auth: state,
        logger: pino({ level: "silent" })
    });
    await socket.ev.on("creds.update", saveCreds);
    await socket.ev.on("connection.update", ({ connection }) => {
            if(connection === "open") console.log("Connet to : " + socket.user.id.split(':')[0]);
            if(connection === "close") connectToWhatsapp();
        });

    // Parsing Message
    await socket.ev.on("messages.upsert", ({ messages }) => {
        const msg = messages[0];
        try {
            //console.log(msg);

            // Reading Message
            function read() {
                const key = {
                    remoteJid: msg.key.remoteJid,
                    id: msg.key.id
                };
                socket.readMessages([key]);
            };

            // Message
           function sendmsg(text) {
                socket.sendMessage(id, { text: text });
            };

            // Reply Message
            function reply(text) {
                socket.sendMessage(msg.key.remoteJid, {text: text}, {quoted: msg}
                );
            };

            // Call Contack
            function mention(text) {
                socket.sendMessage(msg.key.remoteJid, {text: text, mentions:[msg.key.remoteJid]});
            };

            // Reaction
            function react(typ) {
                const reactionMessage = {
                    react: {
                        text: typ, 
                        key: message.key
                    }
                }
                socket.sendMessage(msg.key.remoteJid, reactionMessage)
            }


            const messageType = Object.keys (msg.message)[0];

            console.log(msg);

            if (messageType === 'conversation') {
                read();
                const pesan = msg.message.conversation.toLowerCase();
                
                if (pesan === ".menu") {
                    (async () => {
                        console.log('pesan masuk : ' + pesan);
                        await reply("╔═════ [ *`MENU BOT`* ] ⇒\n║\n║\n╠═ *`DELETE BACKGROUND` :*\n║     [ *1* ] _kirim photo dengan caption :_ \n║             *.removebg*\n║\n║\n╠═ *`STICKER` :*\n║     [ *1* ] _kirim photo dengan caption_ :\n║             *.stiker* [ _untuk photo crop_ ]\n║             *.stiker.FULL* [ _untuk photo FULL_ ]\n║\n║\n╚═ [ _Thanks for using_ ] ♥");  
                    })();

                };

            } else if (messageType === 'extendedTextMessage') (async () => {
                const pesan = msg.message.extendedTextMessage.text;

                if (pesan === ".sticker") (async () => {
                    console.log(pesan);
                    const buffer = await downloadMediaMessage(updatedMediaMsg,'buffer',{ },
                        { 
                            logger,
                            reuploadRequest: socket.updateMediaMessage
                        }
                    );
                    try {
                        await write.writeFile('src/media/download.jpg', buffer);
                        console.log('Succes download media');
                        await rmvbg.rmvbg(socket, msg);
                    } catch (error) {
                        await reply('_Mohon maaf program gagal mendownload file_');
                    }
                })();

            })(); else if (messageType === 'imageMessage') {
                read();
                (async () => {
                    try {
                        caption = msg.message.imageMessage.caption;
                        const buffer = await downloadMediaMessage(msg,'buffer',
                            { },
                            { 
                                logger,
                                reuploadRequest: socket.updateMediaMessage
                            }
                        );
                        
                        if (caption === '.removebg') {
                            try {
                                await write.writeFile('src/media/download.jpg', buffer);
                                console.log('Succes download media');
                                await rmvbg.rmvbg(socket, msg);

                            } catch (error) {
                                await reply('_Mohon maaf program gagal mendownload file_');
                            };


                        } else if (caption.includes('.sticker')) {
                            if (caption === '.sticker') {
                                typ = StickerTypes.CROPPED;
                            } else if (caption === '.sticker.FULL') {
                                typ = StickerTypes.FULL;
                            };

                            try {
                                await write.writeFile('src/media/sticker.png', buffer);
                                console.log('Succes download media');
                                await sticker.stickercreat(socket, msg, typ);

                            } catch (error) {
                                await reply('_Mohon maaf program gagal mendownload file_');
                                console.log(error)
                            };

                        };

                    } catch (error) {
                        console.log('Eror handling');
                    };
                })();
                
            } else if (messageType === 'videoMessage') {
                console.log('pesan video');
                
            } else if (messageType === 'viewOnceMessageV2') (async () => {
                await socket.sendMessage(msg.key.remoteJid, { forward: msg });
                
            })(); else if (msg.key.remoteJid === 'status@broadcast') (async () => {
                console.log('ada status terbaru');
                /*try {
                    await socket.sendMessage('6283846780373@s.whatsapp.net', { forward: msg });
                } catch (err) {
                    console.log(err);
                };*/

            })(); else if (msg.key.fromMe === true) {
                    console.log('pesan masuk : from me');

            };

        } catch (error) {
            console.log(error);
            (async () => {
                const name = msg.pushName;
                const text = `Hi @${msg.key.remoteJid.split('@')[0]},\nmohon maaf *BOT* tidak mengerti pesan anda\nkirim pesan [ .menu ] untuk melihat menu *BOT*\n\n*#sendbyBOT*`;
                //await mention(text);
            })();
        };
    });

};


connectToWhatsapp()
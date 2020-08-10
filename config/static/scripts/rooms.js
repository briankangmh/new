    // Reference to the chat messages area
    let $chatWindow = $("#messages");

    // Our interface to the Chat client
    let chatClient;

    // A handle to the room's chat channel
    let roomChannel;

    // The server will assign the client a random username - stored here
    let username;

    // Helper function to print info messages to the chat window
    function print(infoMessage, asHtml) {
        let $msg = $('<div class="info">');
        if (asHtml) {
            $msg.html(infoMessage);
        } else {
            $msg.text(infoMessage);
        }
        $chatWindow.append($msg);
    }

    // Helper function to print chat message to the chat window
    function printMessage(fromUser, message) {
        let $user = $('<span class="username">').text(fromUser + ":");
        if (fromUser === username) {
            $user.addClass("me");
        }
        let $message = $('<span class="message">').text(message);
        let $container = $('<div class="message-container">');
        $container.append($user).append($message);
        $chatWindow.append($container);
        $chatWindow.scrollTop($chatWindow[0].scrollHeight);
    }

    // Get an access token for the current user, passing a device ID
    // for browser-based apps, we'll just use the value "browser"
    function connectChat(){
 
    $.getJSON(
        `${window.location.origin}/chat/twilio/chat/token/browser`,
        function (data) {
            // Alert the user they have been assigned a random username
            username = data.identity;
            print(
                "You have joined the room with username of: " +
                '<span class="me">' +
                username +
                "</span>",
                true
            );

            // Initialize the Chat client
            Twilio.Chat.Client.create(data.token).then(client => {
                // Use client
                chatClient = client;

                chatClient.getSubscribedChannels().then(createOrJoinChannel);

            });

        }
    );
    }

    // Add the createOrJoinChannel function below this line
    function createOrJoinChannel() {
        // Extract the room's channel name from the page URL
        // let channelName = window.location.pathname.split("/").slice(-2, -1)[0];

        let channelName = question_id + '_' + tutee_id + '_' + tutor_id;

        print(`Attempting to join the "${channelName}" chat channel...`);

        chatClient
            .getChannelByUniqueName(channelName)
            .then(function (channel) {
                roomChannel = channel;
                setupChannel(channelName);
            })
            .catch(function () {
                // If it doesn't exist, let's create it
                chatClient
                    .createChannel({
                        uniqueName: channelName,
                        friendlyName: `${channelName} Chat Channel`
                    })
                    .then(function (channel) {
                        roomChannel = channel;
                        setupChannel(channelName);
                    });
            });
    }

    // Set up channel after it has been found / created
    function setupChannel(name) {
        console.log("setupChannel",name)
        console.log(roomChannel)
        if(roomChannel.state.status !== "joined"){
        roomChannel.join().then(function (channel) {
            print(
                `Joined channel ${name} as <span class="me"> ${username} </span>.`,
                true
            );
            channel.getMessages(30).then(processPage);
        }).catch(function(err) {
            console.error(
              "Couldn't join channel " + roomChannel.friendlyName + ' because ' + err
            );
          });;
        } else {
            roomChannel.getMessages(30).then(processPage);

        }
        // Listen for new messages sent to the channel
        roomChannel.on("messageAdded", function (message) {
            printMessage(message.author, message.body);
        });
    }

    function processPage(page) {
        page.items.forEach(message => {
            printMessage(message.author, message.body);
        });
        if (page.hasNextPage) {
            page.nextPage().then(processPage);
        } else {
            console.log("Done loading messages");
        }
    }

    

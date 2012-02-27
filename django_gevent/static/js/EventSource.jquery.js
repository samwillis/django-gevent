
(function(window){
    
    var EventSource = function(url){
        if (!(this instanceof arguments.callee)){
            throw new TypeError("Constructor cannot be called as a function.");
        }
    
        this.url = url;
        var lastEventId = '';
        var reconnectionTime = 3000;
    
        this.CONNECTING = 0;
        this.OPEN = 0;
        this.CLOSED = 0;
        this.readyState = this.CLOSED;
    
        var events = {};
    
        var that = this;
        var req = null;
    
        this.addEventListener = function(name, func){
            if (!events[name]){
                events[name] = [];
            };
            events[name].push(func);
        };
        
        this.removeEventListener = function(name, func){
            if (events[name]){
                var index = events[name].indexOf(func);
                if(index!=-1) events[name].splice(index, 1);
            };
        };
    
        var fireEvent = function(name, data){
            if (events[name]){
                for (var i=0; i<events[name].length; i++){
                    events[name][i]({
                        data: data,
                        lastEventId: lastEventId,
                        origin: url,
                        req: req,
                        longPoll: true
                    });
                };
            };
        };
    
        var parseEvent = function(event_raw){
            var lines = event_raw.split('\n');
            var event_data = '';
            var event_name = '';
            var key, value;
            for (var i=0; i<lines.length; i++){
                var line = lines[i];
                var split_pos = line.indexOf(':');
                if (split_pos != -1){
                    key = line.slice(0, split_pos);
                    value = line.slice(split_pos+1);
                    if (value.charAt(0)==' '){
                        value = value.slice(1);
                    }
                } else {
                    key = line;
                    value = null;
                }
                if (key=='event'){
                    event_name = value;
                } else if (key=='id'){
                    lastEventId = value;
                } else if (key=='retry'){
                    if (parseInt(value)!=NaN){
                        reconnectionTime = parseInt(value);
                    }
                } else if (key=='data'){
                    if (value){
                        if (event_data){
                            event_data = event_data + '\n' + value
                        } else {
                            event_data = value
                        }
                    }
                }
            };
            if (event_name == ''){
                event_name = 'message';
            }
            fireEvent(event_name, event_data)
        };
    
        var parseData = function(data){
            var raw_events = data.split('\n\n');
            for (var i=0; i<raw_events.length; i++){
                if (raw_events[i]!=''){
                    parseEvent(raw_events[i])
                }
            };
        };
    
        var run = function(){
            that.readyState = this.CONNECTING
            var headers = {
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'x-long-poll': 'true'
            };
            if (lastEventId != ''){
                headers['Last-Event-ID'] = lastEventId;
            };
            req = $.ajax({
                url: url,
                headers: headers,
                success: function(data, textStatus, jqXHR){
                    that.readyState = that.CLOSED;
                    fireEvent('open', {});
                    parseData(data);
                    setTimeout(function(){run()}, reconnectionTime);
                },
                error: function(jqXHR, textStatus, errorThrown){
                    that.readyState = that.CLOSED;
                    fireEvent('error', {});
                }
            });
        };
    
        this.close = function(){
            req.abort();
            this.readyState = this.CLOSED;
        }
    
        run();
    };
    
    if (typeof window.EventSource == 'undefined'){
        window.EventSource = EventSource;
    };
    
})(window);

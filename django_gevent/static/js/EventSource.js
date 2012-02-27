// EventSource.js Copyright (c) 2011, Sam Willis
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//     * Neither the name of Sam Willis nor the names of the contributors may be
//       used to endorse or promote products derived from this software without 
//       specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL SAM WILLIS BE LIABLE FOR ANY DIRECT, INDIRECT, 
// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
// EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

if (typeof window.EventSource == 'undefined'){
(function(window){
    
    var EventSource = function(url){
        
        // Ensure that constructor called with 'new'
        if (!(this instanceof arguments.callee)){
            throw new TypeError("Constructor cannot be called as a function.");
        };
        
        var url = url;
        var lastEventId = '';
        var events_listeners = [];
        var reconnectionTime = 3000;
        
        this.CONNECTING = 0;
        this.OPEN = 0;
        this.CLOSED = 0;
        this.readyState = this.CONNECTING;
        
        this.onopen = null;
        this.onmessage = null;
        this.onerror = null;
        
        var init = function(){
            
        };
        
        this.addEventListener = function(name, func){
            if (!events_listeners[name]) events_listeners[name] = [];
            events_listeners[name].push(func);
        };
        
        this.removeEventListener = function(name, func){
            if (events_listeners[name]){
                var index = events_listeners[name].indexOf(func);
                if(index!=-1) events_listeners[name].splice(index, 1);
            };
        };
    
        this.dispatchEvent = function(name, e){
            var pseudoEvent  = {
                'type': e.type,
                'data': e.data,
                'origin': e.url,
                'lastEventId': e.lastEventId,
                'srcElement': this,
                'target': this,
                'currentTarget': this,
                'eventPhase': 2,
                'bubbles': false,
                'cancelable': false,
                'timeStamp': Date.now(),
                'stopPropagation': function() {},
                'preventDefault': function() {},
                'initEvent': function() {}
            };
            if (name=='open' && this.onopen) this.onopen(pseudoEvent);
            if (name=='message' && this.onmessage) this.onmessage(pseudoEvent);
            if (name=='error' && this.onerror) this.onerror(pseudoEvent);
            if (events_listeners[name]){
                for (var i=0; i<events_listeners[name].length; i++){
                    events_listeners[name][i](pseudoEvent);
                };
            };
        };
        
        this.close = function(){
            
        };
        
        // XMLHttpFactories and createXMLHTTPObject from 
        // http://www.quirksmode.org/js/xmlhttp.html
        var XMLHttpFactories = [
        	function () {return new XMLHttpRequest()},
        	function () {return new ActiveXObject("Msxml2.XMLHTTP")},
        	function () {return new ActiveXObject("Msxml3.XMLHTTP")},
        	function () {return new ActiveXObject("Microsoft.XMLHTTP")}
        ];

        var createXMLHTTPObject = function() {
        	var xmlhttp = false;
        	for (var i=0;i<XMLHttpFactories.length;i++) {
        		try {
        			xmlhttp = XMLHttpFactories[i]();
        		}
        		catch (e) {
        			continue;
        		}
        		break;
        	}
        	return xmlhttp;
        };
        
        init();
    };
    
    window.EventSource = EventSource;
    
})(window);
};
<template>
  <div>
    <textarea id="txt_source" v-model="txt_to_ckeck">
    </textarea>

    <button @click="check_spelling">check</button>
    <div id="txt_destination">{{corrected_text}}
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  data () {
    return {
      corrected_text: '--',
      txt_to_ckeck: ""
    }
  },

  methods: {
    check_spelling: function (txt) {
      var request_data = {
        'text': this.txt_to_ckeck
      }
      console.log("request data: ")
      console.log(request_data)
      axios
        .post('//10.8.0.2:5000/', {text: this.txt_to_ckeck}, {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        })
        .then(response => {
          console.log('POST request completed:')
          console.log(response.data)
          this.corrected_text = response.data.text
          // console.log("sound_file_id=" + response.data.file_id)

          // this.sound_file_id = response.data.file_id;
          // this.imageSrc = "/api/v1/spectrogram?file_id=" + this.sound_file_id
          // this.audioSrc = "/uploads/" + this.sound_file_id + ".wav"
          // console.log("imageSrc: " + this.imageSrc)
          // reader.readAsDataURL(files[0]);
        })
        .catch(function (error) {
          console.log(error) // catch your error
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

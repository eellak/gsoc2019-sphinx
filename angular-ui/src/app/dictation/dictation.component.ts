import { Component, OnInit, OnDestroy } from '@angular/core';
import { AudioRecordingService } from '../recorder.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MyCookieService } from '../cookie.service'
import { ApiService } from '../api.service';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-dictation',
  templateUrl: './dictation.component.html',
  styleUrls: ['./dictation.component.css']
})

export class DictationComponent implements OnDestroy {

  isRecording = false;
  recordedTime;
  blobUrl;
  url;
  clusters: string[];
  decoded_gen: string[];
  decoded_adapt: string[];
  sentence_gen: string;
  sentence_adapt: string;
  errors: string;


  constructor(private httpClient: HttpClient, private audioRecordingService: AudioRecordingService, private sanitizer: DomSanitizer, private cookieServ: MyCookieService, private apiService: ApiService) {
    this.clusters = [];
    this.decoded_gen = [];
    this.decoded_adapt = [];
    this.sentence_gen = "";
    this.sentence_adapt = "";
    this.errors = "";
    sessionStorage.setItem('sentence_gen', this.sentence_gen);
    sessionStorage.setItem('sentence_adapt', this.sentence_adapt);
    sessionStorage.setItem('errors', this.errors);

    this.audioRecordingService.recordingFailed().subscribe(() => {
      this.isRecording = false;
    });

    this.audioRecordingService.getRecordedTime().subscribe((time) => {
      this.recordedTime = time;
    });

    this.audioRecordingService.getRecordedBlob().subscribe((data) => {
      this.url = data.blob;
      this.blobUrl = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(data.blob));
    });
  }

  startRecording() {
    if (!this.isRecording) {
      this.isRecording = true;
      this.audioRecordingService.startRecording();
    }
  }

  abortRecording() {
    if (this.isRecording) {
      this.isRecording = false;
      this.audioRecordingService.abortRecording();
    }
  }

  stopRecording() {
    if (this.isRecording) {
      this.audioRecordingService.stopRecording();
      this.isRecording = false;
    }
  }

  clearRecordedData() {
    this.blobUrl = null;
  }

  ngOnDestroy(): void {
    this.abortRecording();
  }

  getCurrCookie() {
    return this.cookieServ.getCookie()
  }

  getDictation() {
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Access-Control-Allow-Origin', '*');
    headers = headers.append("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    const body = new FormData();
    body.append('cookie', this.getCurrCookie());
    body.append('url', this.url)
    this.apiService.getDictationService(body, headers).subscribe((data) => {
      let temp = JSON.parse(JSON.stringify(data))
      sessionStorage.setItem('decoded_gen', JSON.stringify(temp.text_gen));
      sessionStorage.setItem('decoded_adapt', JSON.stringify(temp.text_adapt));
      sessionStorage.setItem('cluster', JSON.stringify(temp.cluster));
      sessionStorage.setItem('errors', this.getErrors().concat(temp.errors).concat(" "))
      sessionStorage.setItem('sentence_gen', this.getSentenceGen().concat(temp.text_gen).concat(" "))
      sessionStorage.setItem('sentence_adapt', this.getSentenceAdapt().concat(temp.text_adapt).concat(" "))
    })
  }

  getDecodedGen() {
    return JSON.parse(sessionStorage.getItem('decoded_gen'))
  }
  getDecodedAdapt() {
    return JSON.parse(sessionStorage.getItem('decoded_adapt'))
  }

  getCluster() {
    return JSON.parse(sessionStorage.getItem('cluster'))
  }

  getErrors() {
    return sessionStorage.getItem('errors')
  }

  getSentenceGen() {
    return sessionStorage.getItem('sentence_gen')
  }

  getSentenceAdapt() {
    return sessionStorage.getItem('sentence_adapt')
  }



}

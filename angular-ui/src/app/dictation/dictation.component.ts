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
  decoded: string[];
  url;

  constructor(private httpClient: HttpClient, private audioRecordingService: AudioRecordingService, private sanitizer: DomSanitizer, private cookieServ: MyCookieService, private apiService: ApiService) {
    this.decoded = [];

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

  onSubmit(form: NgForm) {
    this.getDictation(form)
  }

  getDictation(form) {
    const body = new FormData();
    body.append('cookie', this.getCurrCookie());
    body.append('method', form.value.lm)
    body.append('url', this.url)
    this.apiService.getDictationService(body).subscribe((data) => {
      this.decoded.push(JSON.parse(JSON.stringify(data)));
      sessionStorage.setItem('decoded', JSON.stringify(this.decoded));
    })
  }

  getDecoded() {
    return JSON.parse(sessionStorage.getItem('decoded'))
  }




}

import { Component, OnInit, OnDestroy } from '@angular/core';
import { AudioRecordingService } from '../recorder.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MyCookieService } from '../cookie.service'
import { ApiService } from '../api.service';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-acoustic-adaptation',
  templateUrl: './acoustic-adaptation.component.html',
  styleUrls: ['./acoustic-adaptation.component.css']
})
export class AcousticAdaptationComponent implements OnDestroy, OnInit {

  isRecording = false;
  recordedTime;
  blobUrl;
  url;
  currEmail;
  reload;
  end;

  constructor(private httpClient: HttpClient, private audioRecordingService: AudioRecordingService, private sanitizer: DomSanitizer, private cookieServ: MyCookieService, private apiService: ApiService) {
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
    this.reload = true;
    this.end = false;
  }

  ngOnInit() { }


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
      this.reload = false;
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

  saveDictation() {
    const body = new FormData();
    body.append('cookie', this.getCurrCookie());
    body.append('url', this.url)
    body.append('text', this.getCurrEmail().email)
    this.apiService.saveDictationService(body).subscribe((data) => {
      this.getEmail();
      this.reload = true;
      this.blobUrl = "";
    })
  }

  getEmail() {
    const body = new FormData();
    body.append('cookie', this.getCurrCookie());
    this.apiService.getEmailService(body).subscribe((data) => {
      sessionStorage.setItem('currEmail', JSON.stringify(data));
    })
  }

  getCurrEmail() {
    return JSON.parse(sessionStorage.getItem('currEmail'))
  }

  adaptAcoustic() {
    const body = new FormData();
    body.append('cookie', this.getCurrCookie());
    this.apiService.adaptAcousticService(body).subscribe((data) => {
      this.end = true;
    })
  }

}

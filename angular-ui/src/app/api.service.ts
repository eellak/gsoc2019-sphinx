import { Injectable, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})

export class ApiService implements OnInit {

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit() {
  }

  public getInfoService(body: HttpParams, headers: HttpHeaders) {
    return this.httpClient.post("http://127.0.0.1:5000/info", body, {
      headers
    })
  }
  public getMessagesService(body: HttpParams, headers: HttpHeaders) {
    return this.httpClient.post("http://127.0.0.1:5000/emails", body, {
      headers
    })
  }

  public getClustersService(body: HttpParams, headers: HttpHeaders) {
    return this.httpClient.post("http://127.0.0.1:5000/clustering", body, {
      headers
    })
  }

  public getDictationService(body: FormData) {
    return this.httpClient.post("http://127.0.0.1:5000/dictation", body)
  }

}

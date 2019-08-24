import { Component, OnInit } from '@angular/core';
import { MyCookieService } from '../cookie.service'
import { ApiService } from '../api.service';
import { NgForm } from '@angular/forms';
import { Options } from 'ng5-slider';
import { HttpParams, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-language-adaptation',
  templateUrl: './language-adaptation.component.html',
  styleUrls: ['./language-adaptation.component.css']
})
export class LanguageAdaptationComponent implements OnInit {
  rangeSliderMinValue: number = 2;
  rangeSliderMaxValue: number = 8;
  rangeSliderOptions: Options = {
    floor: 2,
    ceil: 8
  }
  clusters: any;

  constructor(private cookieServ: MyCookieService, private apiService: ApiService) { }

  ngOnInit() {
  }


  getCurrCookie() {
    return this.cookieServ.getCookie()
  }

  getInfoSession() {
    return JSON.parse(sessionStorage.getItem('info'))
  }


  onSubmit(form: NgForm) {
    this.getClusters(form)
  }

  getClusters(form) {
    let body = new HttpParams().set('cookie', this.getCurrCookie()).set('metric', form.value.metric).set('n_clusters', form.value.n_clusters).set('method', form.value.method).set('min_cl', form.value.min_cl).set('max_cl', form.value.max_cl).set('level', form.value.level)
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers = headers.append('Access-Control-Allow-Origin', '*');
    headers = headers.append("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    this.apiService.getClustersService(body, headers).subscribe((data) => {
      this.clusters = data;
      sessionStorage.setItem('clusters', JSON.stringify(data));
    })
  }

  getClustersSession() {
    return JSON.parse(sessionStorage.getItem('clusters'))
  }
}

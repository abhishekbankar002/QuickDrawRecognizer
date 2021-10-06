/* eslint-disable @typescript-eslint/naming-convention */
/* eslint-disable max-len */
/* eslint-disable @typescript-eslint/member-ordering */
/* eslint-disable prefer-arrow/prefer-arrow-functions */
/* eslint-disable @typescript-eslint/consistent-type-assertions */
// import { Component, OnInit } from '@angular/core';
import { Component, Input, ViewChild, AfterViewInit, ElementRef, OnInit} from '@angular/core';
import { fromEvent } from 'rxjs';
import { switchMap, takeUntil, pairwise } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Platform } from '@ionic/angular';
import { environment } from 'src/environments/environment';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss'],
})
export class PlayComponent implements AfterViewInit {
  @ViewChild('myCanvas') public canvas: ElementRef;


  @Input() public width=500;
  @Input() public height=500;

  coord=[];
  isClicked: any = false;
  className: any;
  labels =['Sun','Flower','Pencil','Umbrella','House','Spoon'];
  selected='';
  x = 'black';
  y = 2;
  private ctx: CanvasRenderingContext2D;

  constructor(private http: HttpClient,private platform: Platform,public alertController: AlertController) { }


  check(){
  }
  ngAfterViewInit(){
    const canvasEl: HTMLCanvasElement = this.canvas.nativeElement;
    this.ctx = <CanvasRenderingContext2D> canvasEl.getContext('2d');
   // canvasEl.width=this.width;
   // canvasEl.height=this.height;
    this.ctx.lineWidth =this.y;
    this.ctx.strokeStyle=this.x;
    this.eventcapture(canvasEl);

  }
  selectedLabel(label){
    this.selected=label;
  }

  private eventcapture(canvasEl: HTMLCanvasElement){

    // if(this.platform.is('desktop')){
      fromEvent(canvasEl, 'mousedown')
      .pipe(
        switchMap((e)=>fromEvent(canvasEl,'mousemove')
          .pipe(
            takeUntil(fromEvent(canvasEl,'mouseup')),
            takeUntil(fromEvent(canvasEl,'mouseleave')),
            pairwise()
          ))
      )
      .subscribe((res: [MouseEvent,MouseEvent])=>{
        const rect=canvasEl.getBoundingClientRect();
        const prevPos={
          x:res[0].clientX - rect.left,
          y:res[0].clientY - rect.top
        };
        const currPos={
          x: res[1].clientX - rect.left,
          y: res[1].clientY - rect.top
        };
        this.draw(prevPos, currPos);
      });
    // }
    // else{
        canvasEl.addEventListener('touchmove', function(e) {
        const touch = e.touches[0];
        e.preventDefault();
        e.stopPropagation();
        const mouseEvent = new MouseEvent('mousemove', {
          clientX: touch.clientX,
          clientY: touch.clientY
        });
        canvasEl.dispatchEvent(mouseEvent);
      }, false);
      canvasEl.addEventListener('touchstart', function(e) {
        const touch = e.touches[0];
        e.preventDefault();
        e.stopPropagation();
        const mouseEvent = new MouseEvent('mousedown', {
          clientX: touch.clientX,
          clientY: touch.clientY
        });
        canvasEl.dispatchEvent(mouseEvent);
      }, false);
    // }

    // this.captureEvents(canvasEl);
    }
    object='';
    private draw(prevPos: {x: number; y: number}, currPos: {x: number; y: number}) {
    if(!this.ctx){ return;}
    this.ctx.beginPath();
    if(prevPos){

    this.ctx.moveTo(prevPos.x, prevPos.y);
    this.ctx.lineTo(currPos.x, currPos.y);
    this.ctx.stroke();
    }
  }

  clear() {

    this.ctx.clearRect(0, 0, this.width, this.height);
    this.coord=[];
  }


  save(){
    const canvas: HTMLCanvasElement=this.canvas.nativeElement;
    const date = Date.now();
    const filename = date + '.png';
    const image = canvas.toDataURL('image/png');
    this.http.post(environment.SERVER_URL + '/play', {filename, image}).subscribe((res: any)=>{
      console.log(res.status, res.className);
      this.showAlert('It is a '+ res.className);
      this.clear();
    });
  }

  showAlert(str) {

    this.alertController.create({
      header: str,
      // subHeader: 'Subtitle for alert',
      // message: str,
      buttons: ['OK']
    }).then(res => {

      res.present();

    });

  }
  // ngOnInit() {}

}

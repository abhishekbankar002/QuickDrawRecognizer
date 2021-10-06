
/* eslint-disable prefer-arrow/prefer-arrow-functions */
/* eslint-disable @typescript-eslint/consistent-type-assertions */
/* eslint-disable @typescript-eslint/naming-convention */
/* eslint-disable max-len */
/* eslint-disable @typescript-eslint/member-ordering */
import { Platform } from '@ionic/angular';
import { Component, Input, ViewChild, AfterViewInit, ElementRef} from '@angular/core';
import { fromEvent } from 'rxjs';
import { switchMap, takeUntil, pairwise } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';


@Component({
  selector: 'app-dataset',
  templateUrl: './dataset.component.html',
  styleUrls: ['./dataset.component.scss']
})
export class DatasetComponent implements AfterViewInit {
  captureEvents: any;
  // coord=[];
  constructor(private http: HttpClient,private platform: Platform) {
    console.log(this.platform.is('desktop'));
   }

  isClicked: any = false;
  className: any;
  button_back='#6666bb';
  labels =['Bird', 'Flower', 'Hand', 'House', 'Pencil', 'Sun', 'Umbrella'];
  selected='';
  check(){
  }
  @ViewChild('myCanvas') public canvas: ElementRef;


  @Input() public width=500;
  @Input() public height=500;

  private ctx: CanvasRenderingContext2D;

  x = 'black';
  y = 2;


  ngAfterViewInit(){
    const canvasEl: HTMLCanvasElement = this.canvas.nativeElement;
    this.ctx = <CanvasRenderingContext2D> canvasEl.getContext('2d');
    this.ctx.lineWidth =this.y;
    this.ctx.strokeStyle=this.x;
    this.eventcapture(canvasEl);
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
  }

  not_updated(){
  }

  object_select(s: string){
    this.className=s;
    this.object='Selected '+this.className;
  }
  selectedLabel(label){
    this.selected=label;
    this.className=this.selected;
    this.object='Selected '+this.className;
  }

  save(){
    if (this.className == null){
      this.not_updated();
      this.object='Select a class';
      return;
    }
    const canvas: HTMLCanvasElement=this.canvas.nativeElement;
    const date = Date.now();
    const filename = this.className + '_' + date + '.png';
    console.log(filename);
    const image = canvas.toDataURL('image/png');
    this.http.post(environment.SERVER_URL + '/dataset', {filename, image, className: this.className }).subscribe((res: any)=>{
      console.log(res.res);
      this.clear();
      this.object=res.res;
    });
  }


}

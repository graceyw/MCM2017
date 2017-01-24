from geojson import loads, Feature, Point, FeatureCollection
from matplotlib import patches, pyplot as plt
from matplotlib.path import Path
from mpl_toolkits.mplot3d import Axes3D
from pandas import DataFrame
from pickle import dumps, dump
from os.path import isfile
from math import log
import seaborn as sns

def plot_zones(data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-122,-122.5)
    ax.set_ylim(37.5,38)
    df = DataFrame()
    for i, zone in enumerate(data['features']):
        plot_zone(zone, ax)
    plt.show()

def plot_zone(zone, ax, color='orange'):
    print zone.properties
    try:
        code = [Path.MOVETO]
        code += (len(zone.geometry['coordinates'][0][0]) - 2)*[Path.LINETO]
        code += [Path.CLOSEPOLY]

        paths = Path(map(tuple, zone.geometry['coordinates'][0][0]), code)
        patch = patches.PathPatch(paths, facecolor=color, lw=2)

        ax.add_patch(patch)
    except:
        pass

def plot_park_distrib(data):
    parks = [z for z in data['features'] if 'OS' in z.properties['znlabel']]
    centroids = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for z in parks:
        xs, ys = tuple(zip(*map(tuple, z.geometry['coordinates'][0][0])))
        x = sum(xs)/len(xs)
        y = sum(ys)/len(ys)
        centroids.append((x,y))
        #plot_zone(z, ax, 'green')
    x_vals = []
    y_vals = []
    z_vals = []
    for i, z in enumerate([z for z in data['features'] if not 'OS' in z.properties['znlabel']]):
        try:
            xs, ys, zs = ([],[],[])
            for x, y in [tuple(p) for p in z.geometry['coordinates'][0][0][::10]]:
                dists = [((px-x)**2+(py-y)**2)**.5 for px, py in centroids]
                dist = min(dists)
                xs.append(x)
                ys.append(y)
                zs.append(dist)
            x_vals.append(xs)
            y_vals.append(ys)
            z_vals.append(zs)
        except:
            pass
    zs = [sum(zs)/len(zs) for zs in z_vals]
    ax.hist(zs, 100)
    plt.show()

def plot_park_distance(data):
    parks = [z for z in data['features'] if 'OS' in z.properties['znlabel']]
    centroids = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for z in parks:
        xs, ys = tuple(zip(*map(tuple, z.geometry['coordinates'][0][0])))
        x = sum(xs)/len(xs)
        y = sum(ys)/len(ys)
        centroids.append((x,y))
        plot_zone(z, ax, 'green')
    x_vals = []
    y_vals = []
    z_vals = []
    for i, z in enumerate([z for z in data['features'] if not 'OS' in z.properties['znlabel']]):
        try:
            for x, y in [tuple(p) for p in z.geometry['coordinates'][0][0][::10]]:
                dists = [((px-x)**2+(py-y)**2)**.5 for px, py in centroids]
                dist = min(dists)
                x_vals.append(x)
                y_vals.append(y)
                z_vals.append(dist)
        except:
            pass
    pts = zip(x_vals, y_vals, z_vals)
    pts = filter(lambda x: x[2]<3*sum(z_vals)/len(z_vals), pts)
    x_vals, y_vals, z_vals = tuple(zip(*pts))
    z_vals = [(z)/max(z_vals) for z in z_vals]
    ax.scatter(x_vals, y_vals, c=z_vals, cmap=plt.get_cmap('cool'))
    plt.show()


if __name__=='__main__':
    data = loads(open('Zoning.geojson').read())
    plot_zones(data)
    plot_park_distance(data)
    plot_park_distrib(data)
